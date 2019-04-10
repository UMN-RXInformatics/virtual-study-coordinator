"""
Virtual Study Coordinator for the Fitbit Study
"""

from flask import flash, request
from salsa.server.admin.views.form_view import FormView
from salsa.server.server import app
from salsa.server.admin.forms import FitbitForm
from salsa.models import db_session, Client, Test, Subject, Visit, Project, FileLink, \
    TestPrototype, TestFileLink, Task, File
from salsa.util import utc_timestamp
from salsa import config
from salsa.server.server import filter_args_by_model
from sqlalchemy.orm.exc import NoResultFound


class FitbitStudyView(FormView):
    """

    """
    title = 'Fitbit Study'
    template = 'fitbit.html'
    Form = FitbitForm
    decorators = []

    def get(self):
        return super(FitbitStudyView, self).get()

    def handle_form(self):
        """
        Validates fitbit form input and checks for a redcap record
        """
        try:
            hr = request.form['hr']
            record = request.form['record']
            event = request.form['event']

            self.attach_file(hr, subject_alias=record, visit_name=event)
            if event == 'eligibility':
                self.template = 'fitbit_complete.html'
            else:
                self.template = 'fitbit_final.html'

            return self.render_app()
            # flash("Couldn't find your survey. Are you sure you're in the right place?")
        except AttributeError:
            flash("Couldn't find your survey. Are you sure you're in the right place?")
            return self.render_app()

    def attach_file(self, contents, subject_alias=None, visit_name=None):
        project = Project.with_id(config['fitbit']['project-id'])

        tp_filter_expr = TestPrototype.project_id.in_([project.id])

        tp_args = filter_args_by_model(TestPrototype, {})
        tp_args['finalized'] = True
        tp_args['kind'] = 'Reading.fitbit.generic'

        test_prototype = TestPrototype.query_one(
            filter_expr=tp_filter_expr,
            filter_by=tp_args
        )

        if not subject_alias or subject_alias == 'null':
            subject_alias = 'default'

        try:
            subject = Subject.query_one(filter_by={
                'project_id': project.id,
                'alias': subject_alias
            })
        except NoResultFound:
            subject = Subject.generate(
                project=project,
                alias=subject_alias)

        db_session.add(subject)
        db_session.flush()

        if not visit_name or visit_name == 'null':
            visit_name = 'default'

        try:
            visit = Visit.query_one(filter_by={
                'subject_id': subject.id,
                'alias': visit_name
            })
        except NoResultFound:
            visit = Visit.generate(
                subject=subject,
                alias=visit_name)

        db_session.add(visit)
        db_session.flush()

        test = Test.generate(visit=visit,
                             test_prototype=test_prototype,
                             audio_quality='clean')
        test.beginning = utc_timestamp()
        db_session.add(test)
        db_session.flush()

        kind = "RawData"
        subclass = "ResponseFile"

        file_obj = File.file_from_contents(contents,
                                           mime_type='text/plain',
                                           original_name='hr.dat')

        db_session.add(file_obj)
        db_session.flush()

        file_link = test.link_file(
            file_obj,
            file_obj.original_name + file_obj.original_extension,
            subclass,
            kind=kind,
            client_id=Client.query_one(filter_by={'username': 'fitbit'}).id
        )

        assert file_link
        db_session.flush()
        index = file_link.create_index()
        db_session.add(index)
        db_session.commit()

app.add_url_rule(
    '/fitbit',
    view_func=FitbitStudyView.as_view('fitbit_study_view')
)
