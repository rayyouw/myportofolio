from django.db import migrations


PROFILE = {
    "name": "Rayhan Fairuz Aqram",
    "npm": "2506586186",
    "study_program": "S1 Ilmu Komputer",
    "bio_intro": "student at Universitas Indonesia.",
    "events_count": 4,
    "organizations_count": 3,
    "focus_areas": ["Data Science", "Artificial Intelligence"],
    "competitions": ["GEMASTIK", "SATRIA DATA"],
    "photo": "/static/img/profile-photo.jpeg",
    "cv_url": "https://drive.google.com/file/d/13_uCOg4YZW9giui-31gChfpYglvTboTC/view?usp=drive_link",
    "linkedin_url": "https://linkedin.com/in/rayhanfairuzaqram",
    "github_url": "https://github.com/rayyouw",
    "email": "rayhanfairuzaqram55@gmail.com",
    "gallery": [
        "/static/img/oh-1.jpeg",
        "/static/img/compfest-2.jpeg",
        "/static/img/pewecuy.jpeg",
        "/static/img/explore-2.jpeg",
        "/static/img/bem-2.jpeg",
        "/static/img/bem-3.jpeg",
        "/static/img/oh-2.jpeg",
    ],
}

EDUCATION = {
    "institution": "Universitas Indonesia",
    "period": "2025 - Now",
    "degree": "Bachelor of Computer Science · GPA 3.69 / 4.00",
    "courses": [
        "Discrete Mathematics 1 & 2",
        "Programming Foundations 1 & 2",
        "Calculus 1 & 2",
        "Introduction to Digital System",
        "Introduction to Computer Organization",
    ],
    "thumbnail": "/static/img/logo-ui.jpeg",
    "order": 1,
}

SKILLS = [
    {
        "title": "Programming",
        "skills": [
            ("Python", "/static/img/python.png"),
            ("C++", "/static/img/c++.png"),
            ("Java", "/static/img/java.png"),
            ("HTML", "/static/img/html.png"),
            ("CSS", "/static/img/css.png"),
        ],
    },
    {
        "title": "Data & Machine Learning",
        "skills": [
            ("pandas", "/static/img/pandas.png"),
            ("NumPy", "/static/img/numpy.png"),
            ("scikit-learn", "/static/img/scikit-learn.png"),
            ("PyTorch", "/static/img/pytorch.png"),
        ],
    },
    {
        "title": "Tools & Productivity",
        "skills": [
            ("Canva", "/static/img/canva.png"),
            ("Microsoft Office", "/static/img/microsoft-office.png"),
            ("Google Workspace", "/static/img/google-workspace.png"),
            ("Google Colab", "/static/img/colab.png"),
            ("Visual Studio Code", "/static/img/vscode.png"),
        ],
    },
    {
        "title": "Spoken Languages",
        "skills": [
            ("Bahasa Indonesia · Native", "/static/img/indonesia.png"),
            ("English · Professional", "/static/img/english.jpg"),
        ],
    },
]

PROJECTS = [
    {
        "title": "Towards Precision Food Self-Sufficiency (Swasembada Pangan): Low-Resource Multimodal Fusion for Food Commodity Land Recommendation from Open Data Source",
        "image": "/static/img/project-1.png",
        "tags": ["Machine Learning", "Computer Vision", "Geospatial Analysis", "Python", "Pytorch"],
        "year": 2026,
        "highlights": [
            "Leveraging pre-trained Convolutional Neural Networks (CNN) and Multilayer Perceptrons (MLP) to seamlessly integrate Sentinel-2 optical satellite imagery with comprehensive biophysical tabular data, enabling the generation of highly precise and integrated land suitability scores.",
            "Integration of WorldCereal agricultural activity data and Sentinel-1 radar imagery synthesizes robust presence labels to mitigate the absence of public datasets, optimizing model training via weighted binary cross-entropy to effectively address class imbalance.",
            "Continued evaluation utilizing spatial cross-validation ensures system reliability across novel regions, while cutting-edge XAI frameworks (SHAP and Grad-CAM) validate agronomical accuracy by identifying critical biophysical limiters and highlighting essential agricultural infrastructure.",
        ],
        "link": "https://drive.google.com/file/d/1FhNL9Kn0hoJR_7mxKKwo-KKJo4QNccVH/view",
        "order": 1,
    },
]


def populate_content(apps, schema_editor):
    profile_model = apps.get_model("main", "Profile")
    profile_model.objects.update_or_create(id=1, defaults=PROFILE)

    education_model = apps.get_model("main", "Education")
    education_model.objects.update_or_create(
        institution=EDUCATION["institution"],
        defaults=EDUCATION,
    )

    category_model = apps.get_model("main", "SkillCategory")
    skill_model = apps.get_model("main", "Skill")
    for category_order, category in enumerate(SKILLS, start=1):
        category_record, _ = category_model.objects.update_or_create(
            title=category["title"],
            defaults={"order": category_order},
        )
        for skill_order, (name, thumbnail) in enumerate(category["skills"], start=1):
            skill_model.objects.update_or_create(
                category=category_record,
                name=name,
                defaults={"thumbnail": thumbnail, "order": skill_order},
            )

    project_model = apps.get_model("main", "Project")
    for project in PROJECTS:
        project_model.objects.update_or_create(
            title=project["title"],
            defaults=project,
        )


def remove_content(apps, schema_editor):
    apps.get_model("main", "Profile").objects.all().delete()
    apps.get_model("main", "Education").objects.all().delete()
    apps.get_model("main", "Skill").objects.all().delete()
    apps.get_model("main", "SkillCategory").objects.all().delete()
    apps.get_model("main", "Project").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_education_profile_project_skillcategory_skill"),
    ]

    operations = [
        migrations.RunPython(populate_content, remove_content),
    ]
