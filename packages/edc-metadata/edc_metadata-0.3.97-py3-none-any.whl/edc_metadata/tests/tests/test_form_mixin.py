from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from edc_appointment.models import Appointment
from edc_consent import site_consents
from edc_facility import import_holidays
from edc_form_validators.form_validator import FormValidator
from edc_lab.models import Panel
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED

from edc_metadata.metadata_helper import MetadataHelperMixin
from edc_metadata.metadata_rules import site_metadata_rules
from edc_metadata.models import CrfMetadata, RequisitionMetadata

from ..consents import consent_v1
from ..models import SubjectConsentV1, SubjectVisit
from ..visit_schedule import visit_schedule
from .test_view_mixin import MyView


class MyForm(MetadataHelperMixin, FormValidator):
    pass


class TestForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def setUp(self):
        site_metadata_rules.registry = {}

        self.user = User.objects.create(username="erik")

        for name in ["one", "two", "three", "four", "five", "six", "seven", "eight"]:
            Panel.objects.create(name=name)

        site_consents.registry = {}
        site_consents.register(consent_v1)
        site_visit_schedules._registry = {}
        site_visit_schedules.loaded = False
        site_visit_schedules.register(visit_schedule)
        self.subject_identifier = "1111111"
        self.assertEqual(CrfMetadata.objects.all().count(), 0)
        self.assertEqual(RequisitionMetadata.objects.all().count(), 0)

        subject_consent = SubjectConsentV1.objects.create(
            subject_identifier=self.subject_identifier, consent_datetime=get_utcnow()
        )
        _, self.schedule = site_visit_schedules.get_by_onschedule_model(
            "edc_metadata.onschedule"
        )
        self.schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=subject_consent.consent_datetime,
        )
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code=self.schedule.visits.first.code,
        )
        self.subject_visit = SubjectVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=self.subject_identifier,
            report_datetime=self.appointment.appt_datetime,
            visit_code=self.appointment.visit_code,
            visit_code_sequence=self.appointment.visit_code_sequence,
            visit_schedule_name=self.appointment.visit_schedule_name,
            schedule_name=self.appointment.schedule_name,
            reason=SCHEDULED,
        )

    def test_ok(self):
        request = RequestFactory().get("/?f=f&e=e&o=o&q=q")
        request.user = self.user
        view = MyView(request=request, appointment=self.appointment)
        self.assertEqual("1000", self.appointment.visit_code)
        view.subject_identifier = self.subject_identifier
        view.kwargs = {}
        context_data = view.get_context_data()
        self.assertEqual(len(context_data.get("crfs")), 5)
        form = MyForm(cleaned_data={}, instance=view.appointment)
        self.assertTrue(form.crf_metadata_exists)
        self.assertTrue(form.crf_metadata_required_exists)
        self.assertTrue(form.requisition_metadata_exists)
        self.assertTrue(form.requisition_metadata_required_exists)
        form.validate()
