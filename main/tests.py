from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Award, Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Teaching Assistant - Fasilkom UI",
            role="Teaching Assistant of Discrete Mathematics 1",
            highlights=["Guided students through discrete mathematics concepts."],
            category="part-time",
        )
        self.award = Award.objects.create(
            title="Data Mining - GEMASTIK 2026",
            description="Finalist at National Level",
            thumbnail="/static/img/logo-gemastik.png",
        )
        self.project = Project.objects.create(
            title="Portfolio Data Dashboard",
            tags=["Django", "Python"],
            year=2026,
            highlights=["Displays portfolio data from the database."],
            link="https://example.com/portfolio-dashboard",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertNotContains(response, self.experience.title)
        self.assertNotContains(response, self.award.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_awards")}"')
        self.assertContains(response, f'href="{reverse("main:show_education")}"')
        self.assertContains(response, f'href="{reverse("main:show_skills")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_education_and_skills_pages(self):
        education_response = self.client.get(reverse("main:show_education"))
        skills_response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(education_response.status_code, 200)
        self.assertTemplateUsed(education_response, "education.html")
        self.assertContains(education_response, "Universitas Indonesia")

        self.assertEqual(skills_response.status_code, 200)
        self.assertTemplateUsed(skills_response, "skills.html")
        self.assertContains(skills_response, "Python")

    def test_projects_page(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.highlights[0])

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, "No projects have been added yet.")

    def test_profile_dynamic_bio_highlights(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, 'bio-number">4+</strong>')
        self.assertContains(response, 'bio-number">3+</strong>')
        self.assertContains(response, 'bio-highlight">GEMASTIK</strong>')
        self.assertContains(response, 'bio-highlight">SATRIA DATA</strong>')

    def test_award_model(self):
        self.assertEqual(str(self.award), self.award.title)

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Teaching Assistant - Fasilkom UI")
        self.assertEqual(
            self.experience.role,
            "Teaching Assistant of Discrete Mathematics 1",
        )
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.role)
        self.assertContains(response, self.experience.highlights[0])
        self.assertContains(response, "Present")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_awards_page(self):
        response = self.client.get(reverse("main:show_awards"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "awards.html")
        self.assertContains(response, self.award.title)
        self.assertContains(response, self.award.description)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, self.experience.ended_at.strftime("%b %Y"))