from django.test import TestCase
from edc_appointment.models import Appointment
from edc_consent import site_consents
from edc_constants.constants import FEMALE, MALE
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_tracking.models import SubjectVisit
from faker import Faker

from edc_metadata.metadata_rules import PF, P

from ..consents import consent_v1
from ..models import CrfOne, SubjectConsentV1
from ..visit_schedule import visit_schedule

fake = Faker()


class TestPredicates(TestCase):
    @classmethod
    def setUpClass(cls):
        import_holidays()
        return super().setUpClass()

    def setUp(self):
        site_consents.registry = {}
        site_consents.register(consent_v1)
        site_visit_schedules._registry = {}
        site_visit_schedules.loaded = False
        site_visit_schedules.register(visit_schedule)

        _, self.schedule = site_visit_schedules.get_by_onschedule_model(
            "edc_metadata.onschedule"
        )

    def enroll(self, gender=None):
        subject_identifier = fake.credit_card_number()
        subject_consent = SubjectConsentV1.objects.create(
            subject_identifier=subject_identifier,
            consent_datetime=get_utcnow(),
            gender=gender,
        )
        self.registered_subject = RegisteredSubject.objects.get(
            subject_identifier=subject_identifier
        )
        self.schedule.put_on_schedule(
            subject_identifier=subject_identifier,
            onschedule_datetime=subject_consent.consent_datetime,
        )
        self.appointment = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code=self.schedule.visits.first.code,
        )
        subject_visit = SubjectVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=subject_identifier,
            report_datetime=self.appointment.appt_datetime,
            visit_code=self.appointment.visit_code,
            visit_code_sequence=self.appointment.visit_code_sequence,
            visit_schedule_name=self.appointment.visit_schedule_name,
            schedule_name=self.appointment.schedule_name,
            reason=SCHEDULED,
        )
        return subject_visit

    def test_p_male(self):
        visit = self.enroll(gender=MALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        self.assertTrue(P("gender", "eq", MALE)(**opts))
        self.assertFalse(P("gender", "eq", FEMALE)(**opts))

    def test_p_female(self):
        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        self.assertTrue(P("gender", "eq", FEMALE)(**opts))
        self.assertFalse(P("gender", "eq", MALE)(**opts))

    def test_p_reason(self):
        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        self.assertTrue(P("reason", "eq", SCHEDULED)(**opts))

    def test_p_with_field_on_source_keyed_value_none(self):
        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        CrfOne.objects.create(subject_visit=visit)
        self.assertFalse(P("f1", "eq", "car")(**opts))

    def test_p_with_field_on_source_keyed_with_value(self):
        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        CrfOne.objects.create(subject_visit=visit, f1="bicycle")
        self.assertFalse(P("f1", "eq", "car")(**opts))

    def test_p_with_field_on_source_keyed_with_matching_value(self):
        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        CrfOne.objects.create(subject_visit=visit, f1="car")
        self.assertTrue(P("f1", "eq", "car")(**opts))

    def test_p_with_field_on_source_keyed_with_multiple_values_in(self):
        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        CrfOne.objects.create(subject_visit=visit, f1="car")
        self.assertTrue(P("f1", "in", ["car", "bicycle"])(**opts))

    def test_p_with_field_on_source_keyed_with_multiple_values_not_in(self):
        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        CrfOne.objects.create(subject_visit=visit, f1="truck")
        self.assertFalse(P("f1", "in", ["car", "bicycle"])(**opts))

    def test_pf(self):
        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        CrfOne.objects.create(subject_visit=visit, f1="car")
        self.assertTrue(PF("f1", func=lambda x: x == "car")(**opts))
        self.assertFalse(PF("f1", func=lambda x: x == "bicycle")(**opts))

    def test_pf_2(self):
        def func(f1, f2):
            return f1 == "car" and f2 == "bicycle"

        visit = self.enroll(gender=FEMALE)
        opts = dict(
            source_model="edc_metadata.crfone",
            registered_subject=self.registered_subject,
            visit=visit,
        )
        CrfOne.objects.create(subject_visit=visit, f1="car", f2="bicycle")
        self.assertTrue(PF("f1", "f2", func=func)(**opts))
