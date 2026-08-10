from datetime import datetime, timezone

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.Text, default="")
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)


class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(40), unique=True, nullable=False)
    label = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(500), default="#")
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class HeroPromise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class ServiceCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.Text)
    description = db.Column(db.Text)
    service_group = db.Column(db.String(40), default="technology")  # technology | digital_marketing
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    items = db.relationship(
        "ServiceItem", backref="category", lazy=True, cascade="all, delete-orphan"
    )


class ServiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("service_category.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(300))
    short_description = db.Column(db.Text)
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(300))
    cta_text = db.Column(db.String(80), default="Try it")
    cta_url = db.Column(db.String(300))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    pricing_sections = db.relationship(
        "ProductPricingSection",
        backref="product",
        lazy=True,
        cascade="all, delete-orphan",
    )
    features = db.relationship(
        "ProductFeature",
        backref="product",
        lazy=True,
        cascade="all, delete-orphan",
    )


class ProductFeature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    text = db.Column(db.String(400), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class ProductPricingSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    rows = db.relationship(
        "ProductPricingRow",
        backref="section",
        lazy=True,
        cascade="all, delete-orphan",
    )


class ProductPricingRow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(
        db.Integer, db.ForeignKey("product_pricing_section.id"), nullable=False
    )
    service_name = db.Column(db.String(300), nullable=False)
    price = db.Column(db.String(200), nullable=False)
    sort_order = db.Column(db.Integer, default=0)


class ClientLogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class WhyChooseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class LearningService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(300))
    cta_text = db.Column(db.String(80), default="Learn More")
    cta_url = db.Column(db.String(300))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class AffiliateStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, default=1)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)


class AffiliateBenefit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)


class AffiliateApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40))
    website = db.Column(db.String(300))
    audience = db.Column(db.Text)
    message = db.Column(db.Text)
    status = db.Column(db.String(40), default="pending")
    created_at = db.Column(db.DateTime, default=utcnow)


class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40))
    country = db.Column(db.String(80))
    looking_for = db.Column(db.Text)
    requirements = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utcnow)


class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    mode = db.Column(db.String(200))
    job_type = db.Column(db.String(80))
    shift = db.Column(db.String(80))
    location = db.Column(db.String(200))
    openings = db.Column(db.Integer, default=1)
    income = db.Column(db.String(200))
    skills = db.Column(db.String(300))
    reference_code = db.Column(db.String(80), unique=True)
    expiry_date = db.Column(db.Date)
    education = db.Column(db.String(200))
    gender = db.Column(db.String(40), default="Any")
    short_description = db.Column(db.Text)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)
    applications = db.relationship(
        "JobApplication", backref="job", lazy=True, cascade="all, delete-orphan"
    )


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_posting.id"), nullable=False)
    application_type = db.Column(db.String(20), default="hiring")
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40))
    email = db.Column(db.String(120))
    current_school = db.Column(db.String(200))
    year_of_study = db.Column(db.String(80))
    address = db.Column(db.Text)
    country = db.Column(db.String(80))
    field_of_study = db.Column(db.String(200))
    timezone = db.Column(db.String(80))
    work_experience = db.Column(db.Text)
    gpa = db.Column(db.String(40))
    resume_filename = db.Column(db.String(300))
    preferred_start = db.Column(db.Date)
    preferred_end = db.Column(db.Date)
    first_internship = db.Column(db.String(20))
    internship_goals = db.Column(db.Text)
    skills_to_demonstrate = db.Column(db.Text)
    working_style = db.Column(db.Text)
    specialization_field = db.Column(db.String(200))
    learn_during_internship = db.Column(db.Text)
    code_of_conduct = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(40), default="Applied")
    company_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(300), unique=True, nullable=False)
    excerpt = db.Column(db.Text)
    content = db.Column(db.Text)
    featured_image = db.Column(db.String(300))
    published_at = db.Column(db.Date)
    sort_order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    message = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)


class ConsultationBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40))
    company = db.Column(db.String(200))
    service_interest = db.Column(db.Text)
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utcnow)


class SuggestionSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40))
    selected_products = db.Column(db.Text)
    selected_services = db.Column(db.Text)
    message = db.Column(db.Text, nullable=False)
    pdf_filename = db.Column(db.String(300))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utcnow)
