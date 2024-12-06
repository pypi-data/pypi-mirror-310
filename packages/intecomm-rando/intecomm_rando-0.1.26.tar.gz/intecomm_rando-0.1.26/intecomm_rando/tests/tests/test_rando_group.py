from __future__ import annotations

import re
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.test import override_settings
from django_mock_queries.query import MockSet
from edc_constants.constants import COMPLETE, NO, UUID_PATTERN, YES
from edc_randomization.site_randomizers import site_randomizers
from edc_registration.models import RegisteredSubject
from edc_sites.single_site import SingleSite
from edc_sites.site import sites
from edc_sites.utils import add_or_update_django_sites
from intecomm_form_validators.tests.mock_models import PatientGroupMockModel
from intecomm_form_validators.tests.test_case_mixin import TestCaseMixin

from intecomm_rando.models import RandomizationList, RegisteredGroup
from intecomm_rando.randomize_group import (
    GroupAlreadyRandomized,
    GroupRandomizationError,
)
from intecomm_rando.randomize_group import RandomizeGroup as BaseRandomizeGroup
from intecomm_rando.randomizers import Randomizer as BaseRandomizer

from ..models import SubjectConsent


class RandomizeGroup(BaseRandomizeGroup):
    subject_consent_model = None

    def subject_consent_model_cls(self, site: Site):
        return SubjectConsent

    def create_group_identifier(self):
        return f"999{str(uuid4())[0:10].upper()}"


@override_settings(
    SITE_ID=101,
    EDC_SITES_AUTODISCOVER_SITES=False,
)
class RandoTests(TestCaseMixin):
    @classmethod
    def setUpTestData(cls):
        class Randomizer(BaseRandomizer):
            randomizationlist_folder = Path(__file__).resolve().parent.parent / "etc"

        sites.initialize(initialize_site_model=True)
        sites.register(
            SingleSite(
                101,
                "kasangati",
                country_code="ug",
                country="uganda",
                language_codes=["en"],
                domain="kasangati.ug.example.com",
            )
        )
        add_or_update_django_sites(verbose=False)
        site_randomizers._registry = {}
        site_randomizers.loaded = False
        site_randomizers.register(Randomizer)

    @override_settings(SITE_ID=101, EDC_SITES_AUTODISCOVER_SITES=False)
    def test_ok(self):
        group_identifier_as_pk = str(uuid4())
        patients = self.get_mock_patients(
            dm=10,
            htn=0,
            hiv=4,
            stable=True,
            screen=True,
            consent=True,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        patient_group = PatientGroupMockModel(
            randomized=False,
            randomize_now=YES,
            confirm_randomize_now="RANDOMIZE",
            group_identifier=group_identifier_as_pk,
            group_identifier_as_pk=group_identifier_as_pk,
            status=COMPLETE,
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        for patient in patient_group.patients.all():
            SubjectConsent.objects.create(
                subject_identifier=patient.subject_identifier,
                site=Site.objects.get(id=settings.SITE_ID),
            )
            RegisteredSubject.objects.create(subject_identifier=patient.subject_identifier)

        self.assertTrue(re.match(UUID_PATTERN, patient_group.group_identifier or ""))
        randomizer = RandomizeGroup(patient_group)
        randomizer.randomize_group()

        self.assertIsNotNone(patient_group.group_identifier)
        self.assertFalse(re.match(UUID_PATTERN, patient_group.group_identifier))
        try:
            RegisteredGroup.objects.get(group_identifier=patient_group.group_identifier)
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised (RegisteredGroup)")

        try:
            RandomizationList.objects.get(group_identifier=patient_group.group_identifier)
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised (RandomizationList)")

    @override_settings(SITE_ID=101)
    def test_already_randomized(self):
        patients = self.get_mock_patients(
            dm=10,
            htn=0,
            hiv=4,
            stable=True,
            screen=True,
            consent=True,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        patient_group = PatientGroupMockModel(
            randomized=True,
            group_identifier="99951518883",
            group_identifier_as_pk=str(uuid4()),
            randomize_now=YES,
            confirm_randomize_now="RANDOMIZE",
            status=COMPLETE,
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        randomizer = RandomizeGroup(patient_group)
        self.assertTrue(patient_group.randomized)
        self.assertRaises(GroupAlreadyRandomized, randomizer.randomize_group)

    @override_settings(SITE_ID=101)
    def test_incomplete_group(self):
        patients = self.get_mock_patients(
            dm=10,
            htn=0,
            hiv=4,
            stable=True,
            screen=True,
            consent=True,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        group_identifier_as_pk = str(uuid4())
        patient_group = PatientGroupMockModel(
            randomized=False,
            randomize_now=YES,
            confirm_randomize_now="RANDOMIZE",
            group_identifier=group_identifier_as_pk,
            group_identifier_as_pk=group_identifier_as_pk,
            status="BLAH",
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        randomizer = RandomizeGroup(patient_group)
        self.assertRaises(GroupRandomizationError, randomizer.randomize_group)
        self.assertFalse(patient_group.randomized)

    @override_settings(SITE_ID=101)
    def test_complete_group_but_not_enough_members(self):
        patients = self.get_mock_patients(
            dm=3,
            htn=0,
            hiv=4,
            stable=True,
            screen=True,
            consent=True,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        group_identifier_as_pk = str(uuid4())
        patient_group = PatientGroupMockModel(
            randomized=False,
            randomize_now=YES,
            confirm_randomize_now="RANDOMIZE",
            group_identifier=group_identifier_as_pk,
            group_identifier_as_pk=group_identifier_as_pk,
            status=COMPLETE,
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        randomizer = RandomizeGroup(patient_group)
        with self.assertRaises(GroupRandomizationError) as cm:
            randomizer.randomize_group()
        self.assertIn("Patient group must have at least", str(cm.exception))
        self.assertFalse(patient_group.randomized)

    @override_settings(SITE_ID=101)
    def test_complete_group_enough_members_not_screened(self):
        patients = self.get_mock_patients(
            dm=4,
            htn=4,
            hiv=4,
            stable=True,
            screen=False,
            consent=False,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        group_identifier_as_pk = str(uuid4())
        patient_group = PatientGroupMockModel(
            randomized=False,
            randomize_now=YES,
            confirm_randomize_now="RANDOMIZE",
            group_identifier=group_identifier_as_pk,
            group_identifier_as_pk=group_identifier_as_pk,
            status=COMPLETE,
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        randomizer = RandomizeGroup(patient_group)
        with self.assertRaises(GroupRandomizationError) as cm:
            randomizer.randomize_group()
        self.assertIn("Patient has not screened", str(cm.exception))
        self.assertFalse(patient_group.randomized)

    @override_settings(SITE_ID=101)
    def test_complete_group_enough_members_not_consented(self):
        patients = self.get_mock_patients(
            dm=4,
            htn=4,
            hiv=4,
            stable=True,
            screen=True,
            consent=False,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        group_identifier_as_pk = str(uuid4())
        patient_group = PatientGroupMockModel(
            randomized=False,
            randomize_now=YES,
            confirm_randomize_now="RANDOMIZE",
            group_identifier=group_identifier_as_pk,
            group_identifier_as_pk=group_identifier_as_pk,
            status=COMPLETE,
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        randomizer = RandomizeGroup(patient_group)
        with self.assertRaises(GroupRandomizationError) as cm:
            randomizer.randomize_group()
        self.assertIn("Patient has not consented", str(cm.exception))
        self.assertFalse(patient_group.randomized)

    @override_settings(SITE_ID=101)
    def test_complete_group_enough_members_all_consented(self):
        group_identifier_as_pk = str(uuid4())
        patients = self.get_mock_patients(
            dm=5,
            htn=5,
            hiv=4,
            stable=True,
            screen=True,
            consent=True,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        patient_group = PatientGroupMockModel(
            randomized=False,
            randomize_now=YES,
            confirm_randomize_now="RANDOMIZE",
            group_identifier=group_identifier_as_pk,
            group_identifier_as_pk=group_identifier_as_pk,
            status=COMPLETE,
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        for patient in patient_group.patients.all():
            SubjectConsent.objects.create(subject_identifier=patient.subject_identifier)
            RegisteredSubject.objects.create(subject_identifier=patient.subject_identifier)
        randomizer = RandomizeGroup(patient_group)
        try:
            randomizer.randomize_group()
        except GroupRandomizationError as e:
            self.fail(f"GroupRandomizationError unexpectedly raised. Got {e}")
        self.assertTrue(patient_group.randomized)

    @override_settings(SITE_ID=101)
    def test_complete_group_but_randomize_now_is_no(self):
        group_identifier_as_pk = str(uuid4())
        patients = self.get_mock_patients(
            dm=5,
            htn=5,
            hiv=4,
            stable=True,
            screen=True,
            consent=True,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        patient_group = PatientGroupMockModel(
            randomized=False,
            randomize_now=YES,
            confirm_randomize_now="RANDOMIZE",
            group_identifier=group_identifier_as_pk,
            group_identifier_as_pk=group_identifier_as_pk,
            status=COMPLETE,
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        for patient in patient_group.patients.all():
            SubjectConsent.objects.create(subject_identifier=patient.subject_identifier)
            RegisteredSubject.objects.create(subject_identifier=patient.subject_identifier)
        randomize_group = RandomizeGroup(patient_group)
        try:
            randomize_group.randomize_group()
        except GroupRandomizationError:
            self.fail("GroupRandomizationError unexpectedly raised.")
        self.assertTrue(patient_group.randomized)

    @override_settings(SITE_ID=101)
    def test_complete_group_enough_members_all_consented_func(self):
        group_identifier_as_pk = str(uuid4())
        patients = self.get_mock_patients(
            dm=5,
            htn=5,
            hiv=4,
            stable=True,
            screen=True,
            consent=True,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        patient_group = PatientGroupMockModel(
            randomized=False,
            randomize_now=NO,
            confirm_randomize_now="RANDOMIZE",
            group_identifier=group_identifier_as_pk,
            group_identifier_as_pk=group_identifier_as_pk,
            status=COMPLETE,
            patients=MockSet(*patients),
            site=Site.objects.get(id=settings.SITE_ID),
        )
        randomize_group = RandomizeGroup(patient_group)
        with self.assertRaises(GroupRandomizationError) as cm:
            randomize_group.randomize_group()
        self.assertIn("Expected YES", str(cm.exception))
        self.assertFalse(patient_group.randomized)
