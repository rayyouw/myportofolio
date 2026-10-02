from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import AwardsForm
from main.models import Award, Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.editor_group, _ = Group.objects.get_or_create(name="Editor")

        self.superuser = User.objects.create_superuser(
            username="owner",
            password="OwnerPassword123!",
            email="owner@example.com",
        )
        self.regular_user = User.objects.create_user(
            username="regular",
            password="RegularPassword123!",
        )
        self.editor_user = User.objects.create_user(
            username="editor",
            password="EditorPassword123!",
        )
        self.editor_user.groups.add(self.editor_group)

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
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="error"')
        self.assertNotContains(response, self.project.title)

    def test_empty_projects_json_returns_empty_array(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

    def test_project_creation_authorization(self):
        project_data = {
            "title": "Protected Project",
            "description": "A protected project",
            "tech_stack": "Django",
            "project_url": "https://example.com/protected",
            "project_image_url": "",
        }

        # 1. Unauthenticated -> redirect to login
        response = self.client.post(reverse("main:create_project"), project_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        # 2. Regular user -> 403 Forbidden
        self.client.force_login(self.regular_user)
        response = self.client.post(reverse("main:create_project"), project_data)
        self.assertEqual(response.status_code, 403)

        # 3. Editor user -> 403 Forbidden (cannot create)
        self.client.force_login(self.editor_user)
        response = self.client.post(reverse("main:create_project"), project_data)
        self.assertEqual(response.status_code, 403)

        # 4. Superuser -> success
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("main:create_project"), project_data)
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Protected Project").exists())

    def test_project_update_authorization(self):
        update_data = {
            "title": "Updated Project",
            "description": "Updated description",
            "tech_stack": "Python, Django",
            "project_url": "https://example.com/updated",
            "project_image_url": "",
        }

        # 1. Unauthenticated -> redirect to login
        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            update_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        # 2. Regular user -> 403 Forbidden
        self.client.force_login(self.regular_user)
        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            update_data,
        )
        self.assertEqual(response.status_code, 403)

        # 3. Editor user -> success
        self.client.force_login(self.editor_user)
        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            update_data,
        )
        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Project")

        # 4. Superuser -> success
        self.client.force_login(self.superuser)
        update_data["title"] = "Superuser Updated"
        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            update_data,
        )
        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Superuser Updated")

    def test_award_deletion_authorization(self):
        award = Award.objects.create(title="Temp Award", description="Temp")

        # 1. Unauthenticated -> 302 redirect
        response = self.client.post(reverse("main:delete_awards", args=[award.id]))
        self.assertEqual(response.status_code, 302)

        # 2. Regular user -> 403 Forbidden
        self.client.force_login(self.regular_user)
        response = self.client.post(reverse("main:delete_awards", args=[award.id]))
        self.assertEqual(response.status_code, 403)

        # 3. Editor -> 403 Forbidden
        self.client.force_login(self.editor_user)
        response = self.client.post(reverse("main:delete_awards", args=[award.id]))
        self.assertEqual(response.status_code, 403)

        # 4. Superuser -> success
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("main:delete_awards", args=[award.id]))
        self.assertRedirects(response, reverse("main:show_awards"))
        self.assertFalse(Award.objects.filter(id=award.id).exists())

    def test_project_deletion_authorization(self):
        project = Project.objects.create(title="Temp Project")

        # 1. Unauthenticated -> 302 redirect
        response = self.client.post(reverse("main:delete_project", args=[project.id]))
        self.assertEqual(response.status_code, 302)

        # 2. Regular user -> 403 Forbidden
        self.client.force_login(self.regular_user)
        response = self.client.post(reverse("main:delete_project", args=[project.id]))
        self.assertEqual(response.status_code, 403)

        # 3. Editor -> 403 Forbidden
        self.client.force_login(self.editor_user)
        response = self.client.post(reverse("main:delete_project", args=[project.id]))
        self.assertEqual(response.status_code, 403)

        # 4. Superuser -> success
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("main:delete_project", args=[project.id]))
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(id=project.id).exists())

    def test_toggle_star(self):
        # 1. Unauthenticated -> redirect to login
        response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        # 2. Regular user can star
        self.client.force_login(self.regular_user)
        response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(self.project.starred_by.filter(id=self.regular_user.id).exists())

        # 3. Regular user can unstar
        response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(self.project.starred_by.filter(id=self.regular_user.id).exists())

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
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="error"')
        self.assertNotContains(response, self.award.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_awards_page_skeleton_is_available_for_every_role(self):
        roles = [None, self.regular_user, self.editor_user, self.superuser]

        for user in roles:
            with self.subTest(role=user.username if user else "anonymous"):
                self.client.logout()
                if user:
                    self.client.force_login(user)

                response = self.client.get(reverse("main:show_awards"))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'id="grid"')
                self.assertContains(response, reverse("main:get_awards_json"))
                self.assertNotContains(response, self.award.title)
                if user and user.is_superuser:
                    self.assertContains(response, 'id="add-award-modal"')
                else:
                    self.assertNotContains(response, 'id="add-award-modal"')

    def test_awards_json_is_public_and_includes_per_user_star_state(self):
        self.award.starred_by.add(self.regular_user)
        roles = [None, self.regular_user, self.editor_user, self.superuser]

        for user in roles:
            with self.subTest(role=user.username if user else "anonymous"):
                self.client.logout()
                if user:
                    self.client.force_login(user)

                response = self.client.get(reverse("main:get_awards_json"))

                self.assertEqual(response.status_code, 200)
                award_json = next(
                    item for item in response.json() if item["pk"] == str(self.award.pk)
                )
                award_data = award_json["fields"]
                self.assertEqual(award_data["title"], self.award.title)
                self.assertEqual(award_data["star_count"], 1)
                self.assertEqual(award_data["is_starred"], user == self.regular_user)

    def test_award_ajax_creation_checks_roles_and_validates_xss_input(self):
        endpoint = reverse("main:create_awards_ajax")
        valid_data = {
            "title": "New Competition Award",
            "description": "First place",
            "thumbnail": "",
        }

        for user in [None, self.regular_user, self.editor_user]:
            with self.subTest(role=user.username if user else "anonymous"):
                self.client.logout()
                if user:
                    self.client.force_login(user)
                response = self.client.post(endpoint, valid_data)
                self.assertEqual(response.status_code, 403)

        self.client.force_login(self.superuser)
        response = self.client.post(endpoint, valid_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Award.objects.filter(title=valid_data["title"]).exists())

        invalid_response = self.client.post(
            endpoint,
            {**valid_data, "title": '<img src="x" onerror="alert(1)">'},
        )
        self.assertEqual(invalid_response.status_code, 400)
        self.assertIn("title", invalid_response.json()["errors"])

    def test_awards_form_strips_html_from_user_text(self):
        form = AwardsForm(
            data={
                "title": "<b>Competition Winner</b>",
                "description": "<p>Won the competition</p>",
                "thumbnail": "",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Competition Winner")
        self.assertEqual(form.cleaned_data["description"], "Won the competition")

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No professional experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, self.experience.ended_at.strftime("%b %Y"))

    def test_auth_views_are_accessible(self):
        response_register = self.client.get(reverse("main:register"))
        response_login = self.client.get(reverse("main:login"))

        self.assertEqual(response_register.status_code, 200)
        self.assertEqual(response_login.status_code, 200)
        self.assertTemplateUsed(response_register, "register.html")
        self.assertTemplateUsed(response_login, "login.html")

    def test_user_can_register_login_and_logout(self):
        register_response = self.client.post(
            reverse("main:register"),
            {"username": "newuser", "password1": "StrongPass123!", "password2": "StrongPass123!"},
        )
        self.assertRedirects(register_response, reverse("main:login"))

        login_response = self.client.post(
            reverse("main:login"),
            {"username": "newuser", "password": "StrongPass123!"},
        )
        self.assertRedirects(login_response, reverse("main:show_main"))
        self.assertIn("sessionid", self.client.cookies)
        self.assertIn("last_login", self.client.cookies)

        logout_response = self.client.get(reverse("main:logout"))
        self.assertRedirects(logout_response, reverse("main:show_main"))
        self.assertFalse(self.client.session.get("_auth_user_id"))
