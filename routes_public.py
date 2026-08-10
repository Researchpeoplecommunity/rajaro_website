import os
from datetime import datetime

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

from helpers import (
    active_social_links,
    format_offerings,
    grouped_services,
    suggestion_form_options,
)
from models import (
    BlogPost,
    ClientLogo,
    ConsultationBooking,
    ContactSubmission,
    HeroPromise,
    JobApplication,
    JobPosting,
    LearningService,
    Product,
    ServiceCategory,
    SuggestionSubmission,
    WhyChooseItem,
    db,
)
from seed import get_content
from utils.uploads import allowed_file, save_document

public_bp = Blueprint("public", __name__)

DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx"}


def upload_folder():
    from flask import current_app
    return current_app.config["UPLOAD_FOLDER"]


def site_context():
    return {
        "site_name": get_content("site_name", "Rajaro Solutions Private Limited"),
        "social_links": active_social_links(),
    }


@public_bp.context_processor
def inject_globals():
    return site_context()


@public_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    folder = upload_folder()
    path = os.path.join(folder, filename)
    if not os.path.isfile(path):
        abort(404)
    return send_from_directory(folder, filename)


@public_bp.route("/health")
def health():
    return {"status": "ok"}, 200


@public_bp.route("/")
def home():
    promises = HeroPromise.query.filter_by(is_active=True).order_by(HeroPromise.sort_order).all()
    return render_template(
        "home.html",
        promises=promises,
        hero_title=get_content("hero_title"),
        hero_subtitle=get_content("hero_subtitle"),
        hero_intro=get_content("hero_intro"),
    )


@public_bp.route("/about")
def about():
    return render_template(
        "about.html",
        what_we_do=get_content("about_what_we_do"),
        who_we_are=get_content("about_who_we_are"),
        mission=get_content("mission"),
        vision=get_content("vision"),
        founder=get_content("about_founder"),
        clients=ClientLogo.query.filter_by(is_active=True).order_by(ClientLogo.sort_order).all(),
        why_items=WhyChooseItem.query.filter_by(is_active=True).order_by(WhyChooseItem.sort_order).all(),
        social_links=active_social_links(),
    )


@public_bp.route("/services")
def services():
    tech_categories, marketing_categories = grouped_services()
    products, service_groups = suggestion_form_options()
    return render_template(
        "services.html",
        tech_categories=tech_categories,
        marketing_categories=marketing_categories,
        products=products,
        service_groups=service_groups,
        services_intro=get_content("services_intro"),
        consultation_headline=get_content("consultation_headline"),
        consultation_text=get_content("consultation_text"),
    )


@public_bp.route("/products")
def products():
    products_list = Product.query.filter_by(is_active=True).order_by(Product.sort_order).all()
    return render_template("products.html", products=products_list)


@public_bp.route("/products/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    features = [f for f in product.features if f.is_active]
    features.sort(key=lambda f: f.sort_order)
    return render_template("product_detail.html", product=product, features=features)


@public_bp.route("/learning")
def learning():
    programs = (
        LearningService.query.filter_by(is_active=True)
        .order_by(LearningService.sort_order)
        .all()
    )
    return render_template(
        "learning.html",
        programs=programs,
        headline=get_content("learning_headline"),
        intro=get_content("learning_intro"),
    )


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or not email:
            if request.headers.get("HX-Request"):
                return render_template("partials/form_error.html", message="Name and email are required.")
            flash("Name and email are required.", "error")
            return redirect(url_for("public.contact"))

        sub = ContactSubmission(
            name=name,
            email=email,
            phone=request.form.get("phone", ""),
            country=request.form.get("country", ""),
            looking_for=format_offerings(request.form.getlist("offerings")),
            requirements=request.form.get("requirements", ""),
        )
        db.session.add(sub)
        db.session.commit()

        if request.headers.get("HX-Request"):
            return render_template(
                "partials/form_success.html",
                message="Thank you! We'll get back to you soon.",
            )
        flash("Message sent successfully!", "success")
        return redirect(url_for("public.contact"))

    products, service_groups = suggestion_form_options()
    return render_template(
        "contact.html",
        address=get_content("contact_address"),
        phone=get_content("contact_phone"),
        email=get_content("contact_email"),
        hours=get_content("contact_hours"),
        products=products,
        service_groups=service_groups,
    )


@public_bp.route("/consultation", methods=["POST"])
def consultation():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    if not name or not email:
        if request.headers.get("HX-Request"):
            return render_template("partials/form_error.html", message="Name and email are required.")
        flash("Name and email are required.", "error")
        return redirect(request.referrer or url_for("public.services"))

    booking = ConsultationBooking(
        name=name,
        email=email,
        phone=request.form.get("phone", ""),
        company=request.form.get("company", ""),
        service_interest=format_offerings(request.form.getlist("offerings")),
        message=request.form.get("message", ""),
    )
    db.session.add(booking)
    db.session.commit()

    if request.headers.get("HX-Request"):
        return render_template(
            "partials/form_success.html",
            message="Consultation request received! Our team will contact you shortly.",
        )
    flash("Consultation booked!", "success")
    return redirect(request.referrer or url_for("public.services"))


@public_bp.route("/suggestions", methods=["GET", "POST"])
def suggestions():
    products, service_groups = suggestion_form_options()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        selected_products = []
        selected_services = []
        for offering in request.form.getlist("offerings"):
            if offering.startswith("p:"):
                selected_products.append(offering[2:])
            elif offering.startswith("s:"):
                selected_services.append(offering[2:])

        def form_error(msg):
            if request.headers.get("HX-Request"):
                return render_template("partials/form_error.html", message=msg)
            flash(msg, "error")
            return redirect(url_for("public.suggestions"))

        if not name or not email:
            return form_error("Name and email are required.")
        if not selected_products and not selected_services:
            return form_error("Please select at least one product or service.")
        if not message:
            return form_error("Please write your suggestion.")
        if "pdf" not in request.files or not request.files["pdf"].filename:
            return form_error("Please attach a PDF file.")
        if not allowed_file(request.files["pdf"].filename, {"pdf"}):
            return form_error("Only PDF files are allowed.")

        pdf_filename = save_document(request.files["pdf"], prefix="suggestion")
        if not pdf_filename:
            return form_error("Could not upload PDF. Please try again.")

        submission = SuggestionSubmission(
            name=name,
            email=email,
            phone=request.form.get("phone", ""),
            selected_products=", ".join(selected_products),
            selected_services=", ".join(selected_services),
            message=message,
            pdf_filename=pdf_filename,
        )
        db.session.add(submission)
        db.session.commit()

        if request.headers.get("HX-Request"):
            return render_template(
                "partials/form_success.html",
                message="Thank you! Your suggestion has been submitted successfully.",
            )
        flash("Suggestion submitted successfully!", "success")
        return redirect(url_for("public.suggestions"))

    return render_template(
        "suggestion.html",
        products=products,
        service_groups=service_groups,
    )


@public_bp.route("/career")
def career():
    jobs = JobPosting.query.filter_by(is_active=True).order_by(JobPosting.created_at.desc()).all()
    return render_template("career.html", jobs=jobs)


@public_bp.route("/career/<int:job_id>")
def job_detail(job_id):
    job = JobPosting.query.filter_by(id=job_id, is_active=True).first_or_404()
    return render_template("job_detail.html", job=job)


@public_bp.route("/career/<int:job_id>/apply", methods=["GET", "POST"])
def job_apply(job_id):
    job = JobPosting.query.filter_by(id=job_id, is_active=True).first_or_404()
    app_type = request.args.get("type", "hiring")

    if request.method == "POST":
        app_type = request.form.get("application_type", "hiring")
        full_name = request.form.get("full_name", "").strip()
        if not full_name:
            if request.headers.get("HX-Request"):
                return render_template("partials/form_error.html", message="Full name is required.")
            flash("Full name is required.", "error")
            return redirect(url_for("public.job_apply", job_id=job_id, type=app_type))

        resume_filename = None
        if "resume" in request.files:
            file = request.files["resume"]
            if file and file.filename and allowed_file(file.filename, DOCUMENT_EXTENSIONS):
                folder = upload_folder()
                os.makedirs(folder, exist_ok=True)
                resume_filename = secure_filename(f"{job.reference_code}_{file.filename}")
                file.save(os.path.join(folder, resume_filename))

        def parse_date(val):
            if not val:
                return None
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except ValueError:
                return None

        application = JobApplication(
            job_id=job.id,
            application_type=app_type,
            full_name=full_name,
            phone=request.form.get("phone", ""),
            email=request.form.get("email", ""),
            current_school=request.form.get("current_school", ""),
            year_of_study=request.form.get("year_of_study", ""),
            address=request.form.get("address", ""),
            country=request.form.get("country", ""),
            field_of_study=request.form.get("field_of_study", ""),
            timezone=request.form.get("timezone", ""),
            work_experience=request.form.get("work_experience", ""),
            gpa=request.form.get("gpa", ""),
            resume_filename=resume_filename,
            preferred_start=parse_date(request.form.get("preferred_start")),
            preferred_end=parse_date(request.form.get("preferred_end")),
            first_internship=request.form.get("first_internship", ""),
            internship_goals=request.form.get("internship_goals", ""),
            skills_to_demonstrate=request.form.get("skills_to_demonstrate", ""),
            working_style=request.form.get("working_style", ""),
            specialization_field=request.form.get("specialization_field", ""),
            learn_during_internship=request.form.get("learn_during_internship", ""),
            code_of_conduct="code_of_conduct" in request.form,
            status="Applied",
        )
        db.session.add(application)
        db.session.commit()

        if request.headers.get("HX-Request"):
            return render_template(
                "partials/form_success.html",
                message="Application submitted successfully!",
            )
        flash("Application submitted!", "success")
        return redirect(url_for("public.job_detail", job_id=job_id))

    return render_template("job_apply.html", job=job, app_type=app_type)


@public_bp.route("/blog")
def blog():
    posts = (
        BlogPost.query.filter_by(is_published=True)
        .order_by(BlogPost.sort_order, BlogPost.published_at.desc())
        .all()
    )
    return render_template("blog.html", posts=posts)


@public_bp.route("/blog/<slug>")
def blog_detail(slug):
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template("blog_detail.html", post=post)


@public_bp.route("/search")
def search():
    q = request.args.get("q", "").strip().lower()
    results = {"jobs": [], "blogs": [], "services": []}
    if q:
        results["jobs"] = JobPosting.query.filter(
            JobPosting.is_active == True,  # noqa: E712
            db.or_(
                JobPosting.title.ilike(f"%{q}%"),
                JobPosting.skills.ilike(f"%{q}%"),
            ),
        ).all()
        results["blogs"] = BlogPost.query.filter(
            BlogPost.is_published == True,  # noqa: E712
            db.or_(
                BlogPost.title.ilike(f"%{q}%"),
                BlogPost.excerpt.ilike(f"%{q}%"),
            ),
        ).all()
        results["services"] = ServiceCategory.query.filter(
            ServiceCategory.is_active == True,  # noqa: E712
            db.or_(
                ServiceCategory.title.ilike(f"%{q}%"),
                ServiceCategory.description.ilike(f"%{q}%"),
            ),
        ).all()
    return render_template("search.html", query=q, results=results)
