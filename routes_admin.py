import os
import re
from datetime import datetime
from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from config import Config
from models import (
    AdminUser,
    AffiliateApplication,
    AffiliateBenefit,
    AffiliateStep,
    BlogPost,
    ClientLogo,
    ConsultationBooking,
    ContactSubmission,
    HeroPromise,
    JobApplication,
    JobPosting,
    LearningService,
    Notification,
    Product,
    ProductPricingRow,
    ProductPricingSection,
    ServiceCategory,
    ServiceItem,
    SiteContent,
    SuggestionSubmission,
    WhyChooseItem,
    db,
)
from seed import get_content, set_content

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


def upload_folder():
    from flask import current_app
    return current_app.config["UPLOAD_FOLDER"]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text).strip("-")


@admin_bp.before_request
def require_admin_login():
    """Force authentication for every admin route except the login page."""
    if request.endpoint == "admin.login":
        return None
    if not current_user.is_authenticated:
        return redirect(url_for("admin.login", next=request.url))
    return None


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)

    return decorated


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=False)
            next_page = request.args.get("next") or request.form.get("next")
            if next_page and next_page.startswith("/admin"):
                return redirect(next_page)
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = {
        "contacts": ContactSubmission.query.count(),
        "unread_contacts": ContactSubmission.query.filter_by(is_read=False).count(),
        "affiliates": AffiliateApplication.query.count(),
        "applications": JobApplication.query.count(),
        "consultations": ConsultationBooking.query.count(),
        "suggestions": SuggestionSubmission.query.count(),
        "unread_suggestions": SuggestionSubmission.query.filter_by(is_read=False).count(),
        "blogs": BlogPost.query.count(),
        "jobs": JobPosting.query.filter_by(is_active=True).count(),
    }
    recent_contacts = ContactSubmission.query.order_by(ContactSubmission.created_at.desc()).limit(5).all()
    recent_apps = JobApplication.query.order_by(JobApplication.created_at.desc()).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_contacts=recent_contacts,
        recent_apps=recent_apps,
    )


@admin_bp.route("/content", methods=["GET", "POST"])
@admin_required
def content():
    if request.method == "POST":
        for key in request.form:
            if key.startswith("content_"):
                field_key = key.replace("content_", "", 1)
                set_content(field_key, request.form[key])
        db.session.commit()
        flash("Site content updated.", "success")
        return redirect(url_for("admin.content"))
    content_rows = {c.key: c.value for c in SiteContent.query.all()}
    promises = HeroPromise.query.order_by(HeroPromise.sort_order).all()
    return render_template("admin/content.html", content=content_rows, promises=promises)


@admin_bp.route("/promises/add", methods=["POST"])
@admin_required
def add_promise():
    text = request.form.get("text", "").strip()
    if text:
        max_order = db.session.query(db.func.max(HeroPromise.sort_order)).scalar() or 0
        db.session.add(HeroPromise(text=text, sort_order=max_order + 1))
        db.session.commit()
    return redirect(url_for("admin.content"))


@admin_bp.route("/promises/<int:pid>/delete", methods=["POST"])
@admin_required
def delete_promise(pid):
    p = HeroPromise.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for("admin.content"))


@admin_bp.route("/services")
@admin_required
def services():
    categories = ServiceCategory.query.order_by(ServiceCategory.sort_order).all()
    return render_template("admin/services.html", categories=categories)


@admin_bp.route("/services/category", methods=["POST"])
@admin_required
def add_category():
    title = request.form.get("title", "").strip()
    if title:
        max_order = db.session.query(db.func.max(ServiceCategory.sort_order)).scalar() or 0
        cat = ServiceCategory(
            title=title,
            subtitle=request.form.get("subtitle", ""),
            description=request.form.get("description", ""),
            service_group=request.form.get("service_group", "technology"),
            sort_order=max_order + 1,
        )
        db.session.add(cat)
        db.session.commit()
    return redirect(url_for("admin.services"))


@admin_bp.route("/services/category/<int:cid>", methods=["GET", "POST"])
@admin_required
def edit_category(cid):
    cat = ServiceCategory.query.get_or_404(cid)
    if request.method == "POST":
        cat.title = request.form.get("title", cat.title)
        cat.subtitle = request.form.get("subtitle", "")
        cat.description = request.form.get("description", "")
        cat.service_group = request.form.get("service_group", cat.service_group)
        cat.is_active = "is_active" in request.form
        db.session.commit()
        flash("Category updated.", "success")
        return redirect(url_for("admin.edit_category", cid=cid))
    return render_template("admin/edit_category.html", category=cat)


@admin_bp.route("/services/category/<int:cid>/item", methods=["POST"])
@admin_required
def add_service_item(cid):
    name = request.form.get("name", "").strip()
    if name:
        max_order = (
            db.session.query(db.func.max(ServiceItem.sort_order))
            .filter_by(category_id=cid)
            .scalar()
            or 0
        )
        db.session.add(ServiceItem(category_id=cid, name=name, sort_order=max_order + 1))
        db.session.commit()
    return redirect(url_for("admin.edit_category", cid=cid))


@admin_bp.route("/services/item/<int:iid>/delete", methods=["POST"])
@admin_required
def delete_service_item(iid):
    item = ServiceItem.query.get_or_404(iid)
    cid = item.category_id
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("admin.edit_category", cid=cid))


@admin_bp.route("/products")
@admin_required
def products():
    products_list = Product.query.order_by(Product.sort_order).all()
    return render_template("admin/products.html", products=products_list)


@admin_bp.route("/products/<int:pid>", methods=["GET", "POST"])
@admin_required
def edit_product(pid):
    product = Product.query.get_or_404(pid)
    if request.method == "POST":
        product.name = request.form.get("name", product.name)
        product.tagline = request.form.get("tagline", "")
        product.short_description = request.form.get("short_description", "")
        product.description = request.form.get("description", "")
        product.cta_text = request.form.get("cta_text", "Try it")
        product.cta_url = request.form.get("cta_url", "")
        product.is_active = "is_active" in request.form
        if "image" in request.files and request.files["image"].filename:
            from utils.uploads import save_upload
            product.image_filename = save_upload(request.files["image"], "product")
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("admin.edit_product", pid=pid))
    return render_template("admin/edit_product.html", product=product)


@admin_bp.route("/products/<int:pid>/pricing", methods=["POST"])
@admin_required
def add_pricing_section(pid):
    title = request.form.get("title", "").strip()
    if title:
        max_order = (
            db.session.query(db.func.max(ProductPricingSection.sort_order))
            .filter_by(product_id=pid)
            .scalar()
            or 0
        )
        db.session.add(ProductPricingSection(product_id=pid, title=title, sort_order=max_order + 1))
        db.session.commit()
    return redirect(url_for("admin.edit_product", pid=pid))


@admin_bp.route("/products/pricing/<int:sid>/row", methods=["POST"])
@admin_required
def add_pricing_row(sid):
    section = ProductPricingSection.query.get_or_404(sid)
    service_name = request.form.get("service_name", "").strip()
    price = request.form.get("price", "").strip()
    if service_name and price:
        max_order = (
            db.session.query(db.func.max(ProductPricingRow.sort_order))
            .filter_by(section_id=sid)
            .scalar()
            or 0
        )
        db.session.add(
            ProductPricingRow(
                section_id=sid, service_name=service_name, price=price, sort_order=max_order + 1
            )
        )
        db.session.commit()
    return redirect(url_for("admin.edit_product", pid=section.product_id))


@admin_bp.route("/about", methods=["GET", "POST"])
@admin_required
def about():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "client":
            name = request.form.get("client_name", "").strip()
            if name:
                db.session.add(ClientLogo(name=name))
                db.session.commit()
        elif action == "why":
            text = request.form.get("why_text", "").strip()
            if text:
                max_order = db.session.query(db.func.max(WhyChooseItem.sort_order)).scalar() or 0
                db.session.add(WhyChooseItem(text=text, sort_order=max_order + 1))
                db.session.commit()
        elif action == "content":
            for key in ("about_what_we_do", "about_who_we_are", "mission", "vision", "about_founder"):
                if key in request.form:
                    set_content(key, request.form[key])
            db.session.commit()
            flash("About content updated.", "success")
    clients = ClientLogo.query.order_by(ClientLogo.sort_order).all()
    why_items = WhyChooseItem.query.order_by(WhyChooseItem.sort_order).all()
    content = {c.key: c.value for c in SiteContent.query.filter(SiteContent.key.like("about_%")).all()}
    content.update({c.key: c.value for c in SiteContent.query.filter(SiteContent.key.in_(["mission", "vision"])).all()})
    return render_template("admin/about.html", clients=clients, why_items=why_items, content=content)


@admin_bp.route("/learning", methods=["GET", "POST"])
@admin_required
def learning():
    if request.method == "POST":
        action = request.form.get("action", "content")
        if action == "content":
            for key in ("learning_headline", "learning_intro"):
                if key in request.form:
                    set_content(key, request.form[key])
            db.session.commit()
            flash("Learning section updated.", "success")
        elif action == "add":
            title = request.form.get("service_title", "").strip()
            desc = request.form.get("service_description", "")
            if title:
                from utils.uploads import save_upload
                max_order = db.session.query(db.func.max(LearningService.sort_order)).scalar() or 0
                program = LearningService(
                    title=title,
                    description=desc,
                    cta_text=request.form.get("cta_text", "Learn More"),
                    cta_url=request.form.get("cta_url", ""),
                    sort_order=max_order + 1,
                )
                if "image" in request.files and request.files["image"].filename:
                    program.image_filename = save_upload(request.files["image"], "learning")
                db.session.add(program)
                db.session.commit()
                flash("Learning program added.", "success")
    services = LearningService.query.order_by(LearningService.sort_order).all()
    content = {
        "learning_headline": get_content("learning_headline"),
        "learning_intro": get_content("learning_intro"),
    }
    return render_template("admin/learning.html", services=services, content=content)


@admin_bp.route("/affiliate", methods=["GET", "POST"])
@admin_required
def affiliate_admin():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "content":
            for key in ("affiliate_headline", "affiliate_cta", "affiliate_email"):
                if key in request.form:
                    set_content(key, request.form[key])
        elif action == "step":
            db.session.add(
                AffiliateStep(
                    step_number=int(request.form.get("step_number", 1)),
                    title=request.form.get("title", ""),
                    description=request.form.get("description", ""),
                )
            )
        elif action == "benefit":
            db.session.add(
                AffiliateBenefit(
                    title=request.form.get("title", ""),
                    description=request.form.get("description", ""),
                )
            )
        db.session.commit()
        flash("Affiliate section updated.", "success")
    steps = AffiliateStep.query.order_by(AffiliateStep.sort_order).all()
    benefits = AffiliateBenefit.query.order_by(AffiliateBenefit.sort_order).all()
    applications = AffiliateApplication.query.order_by(AffiliateApplication.created_at.desc()).all()
    content = {
        "affiliate_headline": get_content("affiliate_headline"),
        "affiliate_cta": get_content("affiliate_cta"),
        "affiliate_email": get_content("affiliate_email"),
    }
    return render_template(
        "admin/affiliate.html",
        steps=steps,
        benefits=benefits,
        applications=applications,
        content=content,
    )


@admin_bp.route("/affiliate/applications/<int:aid>/status", methods=["POST"])
@admin_required
def update_affiliate_status(aid):
    app = AffiliateApplication.query.get_or_404(aid)
    app.status = request.form.get("status", app.status)
    db.session.commit()
    return redirect(url_for("admin.affiliate_admin"))


@admin_bp.route("/contact", methods=["GET", "POST"])
@admin_required
def contact_admin():
    if request.method == "POST":
        for key in ("contact_address", "contact_phone", "contact_email", "contact_hours"):
            if key in request.form:
                set_content(key, request.form[key])
        db.session.commit()
        flash("Contact details updated.", "success")
    submissions = ContactSubmission.query.order_by(ContactSubmission.created_at.desc()).all()
    content = {
        "contact_address": get_content("contact_address"),
        "contact_phone": get_content("contact_phone"),
        "contact_email": get_content("contact_email"),
        "contact_hours": get_content("contact_hours"),
    }
    return render_template("admin/contact.html", submissions=submissions, content=content)


@admin_bp.route("/contact/<int:cid>/read", methods=["POST"])
@admin_required
def mark_contact_read(cid):
    sub = ContactSubmission.query.get_or_404(cid)
    sub.is_read = True
    db.session.commit()
    return redirect(url_for("admin.contact_admin"))


@admin_bp.route("/consultations")
@admin_required
def consultations():
    bookings = ConsultationBooking.query.order_by(ConsultationBooking.created_at.desc()).all()
    return render_template("admin/consultations.html", bookings=bookings)


@admin_bp.route("/suggestions")
@admin_required
def suggestions_admin():
    submissions = SuggestionSubmission.query.order_by(SuggestionSubmission.created_at.desc()).all()
    return render_template("admin/suggestions.html", submissions=submissions)


@admin_bp.route("/suggestions/<int:sid>")
@admin_required
def view_suggestion(sid):
    submission = SuggestionSubmission.query.get_or_404(sid)
    if not submission.is_read:
        submission.is_read = True
        db.session.commit()
    return render_template("admin/view_suggestion.html", submission=submission)


@admin_bp.route("/suggestions/<int:sid>/read", methods=["POST"])
@admin_required
def mark_suggestion_read(sid):
    submission = SuggestionSubmission.query.get_or_404(sid)
    submission.is_read = True
    db.session.commit()
    return redirect(url_for("admin.suggestions_admin"))


@admin_bp.route("/suggestions/<int:sid>/delete", methods=["POST"])
@admin_required
def delete_suggestion(sid):
    submission = SuggestionSubmission.query.get_or_404(sid)
    db.session.delete(submission)
    db.session.commit()
    flash("Suggestion deleted.", "success")
    return redirect(url_for("admin.suggestions_admin"))


@admin_bp.route("/jobs")
@admin_required
def jobs():
    jobs_list = JobPosting.query.order_by(JobPosting.created_at.desc()).all()
    return render_template("admin/jobs.html", jobs=jobs_list)


@admin_bp.route("/jobs/add", methods=["GET", "POST"])
@admin_required
def add_job():
    if request.method == "POST":
        expiry = request.form.get("expiry_date")
        job = JobPosting(
            title=request.form.get("title", ""),
            mode=request.form.get("mode", ""),
            job_type=request.form.get("job_type", ""),
            shift=request.form.get("shift", ""),
            location=request.form.get("location", ""),
            openings=int(request.form.get("openings", 1) or 1),
            income=request.form.get("income", ""),
            skills=request.form.get("skills", ""),
            reference_code=request.form.get("reference_code", ""),
            expiry_date=datetime.strptime(expiry, "%Y-%m-%d").date() if expiry else None,
            education=request.form.get("education", ""),
            gender=request.form.get("gender", "Any"),
            short_description=request.form.get("short_description", ""),
            description=request.form.get("description", ""),
            is_active="is_active" in request.form,
        )
        db.session.add(job)
        db.session.commit()
        flash("Job posted.", "success")
        return redirect(url_for("admin.jobs"))
    return render_template("admin/add_job.html")


@admin_bp.route("/jobs/<int:jid>", methods=["GET", "POST"])
@admin_required
def edit_job(jid):
    job = JobPosting.query.get_or_404(jid)
    if request.method == "POST":
        expiry = request.form.get("expiry_date")
        job.title = request.form.get("title", job.title)
        job.mode = request.form.get("mode", "")
        job.job_type = request.form.get("job_type", "")
        job.shift = request.form.get("shift", "")
        job.location = request.form.get("location", "")
        job.openings = int(request.form.get("openings", 1) or 1)
        job.income = request.form.get("income", "")
        job.skills = request.form.get("skills", "")
        job.reference_code = request.form.get("reference_code", "")
        job.expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date() if expiry else None
        job.education = request.form.get("education", "")
        job.gender = request.form.get("gender", "Any")
        job.short_description = request.form.get("short_description", "")
        job.description = request.form.get("description", "")
        job.is_active = "is_active" in request.form
        db.session.commit()
        flash("Job updated.", "success")
        return redirect(url_for("admin.edit_job", jid=jid))
    return render_template("admin/edit_job.html", job=job)


@admin_bp.route("/applications")
@admin_required
def applications():
    apps = JobApplication.query.order_by(JobApplication.created_at.desc()).all()
    return render_template("admin/applications.html", applications=apps)


@admin_bp.route("/applications/<int:aid>", methods=["GET", "POST"])
@admin_required
def view_application(aid):
    app = JobApplication.query.get_or_404(aid)
    if request.method == "POST":
        app.status = request.form.get("status", app.status)
        app.company_notes = request.form.get("company_notes", "")
        db.session.commit()
        flash("Application updated.", "success")
        return redirect(url_for("admin.view_application", aid=aid))
    return render_template("admin/view_application.html", application=app)


@admin_bp.route("/blogs")
@admin_required
def blogs():
    posts = BlogPost.query.order_by(BlogPost.sort_order, BlogPost.published_at.desc()).all()
    return render_template("admin/blogs.html", posts=posts)


@admin_bp.route("/blogs/add", methods=["GET", "POST"])
@admin_required
def add_blog():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = slugify(request.form.get("slug") or title)
        pub = request.form.get("published_at")
        post = BlogPost(
            title=title,
            slug=slug,
            excerpt=request.form.get("excerpt", ""),
            content=request.form.get("content", ""),
            published_at=datetime.strptime(pub, "%Y-%m-%d").date() if pub else None,
            is_published="is_published" in request.form,
            sort_order=int(request.form.get("sort_order", 0) or 0),
        )
        if "featured_image" in request.files and request.files["featured_image"].filename:
            from utils.uploads import save_upload
            post.featured_image = save_upload(request.files["featured_image"], "blog")
        db.session.add(post)
        db.session.commit()
        flash("Blog post created.", "success")
        return redirect(url_for("admin.blogs"))
    return render_template("admin/add_blog.html")


@admin_bp.route("/blogs/<int:bid>", methods=["GET", "POST"])
@admin_required
def edit_blog(bid):
    post = BlogPost.query.get_or_404(bid)
    if request.method == "POST":
        post.title = request.form.get("title", post.title)
        post.slug = slugify(request.form.get("slug") or post.title)
        pub = request.form.get("published_at")
        post.excerpt = request.form.get("excerpt", "")
        post.content = request.form.get("content", "")
        post.published_at = datetime.strptime(pub, "%Y-%m-%d").date() if pub else None
        post.is_published = "is_published" in request.form
        post.sort_order = int(request.form.get("sort_order", post.sort_order or 0))
        if "featured_image" in request.files and request.files["featured_image"].filename:
            from utils.uploads import save_upload
            post.featured_image = save_upload(request.files["featured_image"], "blog")
        db.session.commit()
        flash("Blog post updated.", "success")
        return redirect(url_for("admin.edit_blog", bid=bid))
    return render_template("admin/edit_blog.html", post=post)


@admin_bp.route("/notifications", methods=["GET", "POST"])
@admin_required
def notifications():
    if request.method == "POST":
        db.session.add(
            Notification(
                title=request.form.get("title", ""),
                message=request.form.get("message", ""),
                is_active="is_active" in request.form,
            )
        )
        db.session.commit()
        flash("Notification added.", "success")
        return redirect(url_for("admin.notifications"))
    notifs = Notification.query.order_by(Notification.created_at.desc()).all()
    return render_template("admin/notifications.html", notifications=notifs)


@admin_bp.route("/notifications/<int:nid>/toggle", methods=["POST"])
@admin_required
def toggle_notification(nid):
    n = Notification.query.get_or_404(nid)
    n.is_active = not n.is_active
    db.session.commit()
    return redirect(url_for("admin.notifications"))
