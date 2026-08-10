"""Extended admin CMS routes — social, products, learning, blogs, services."""

from datetime import datetime

from flask import flash, redirect, render_template, request, url_for

from models import (
    BlogPost,
    LearningService,
    Product,
    ProductFeature,
    ServiceCategory,
    ServiceItem,
    SocialLink,
    WhyChooseItem,
    db,
)
from routes_admin import admin_bp, admin_required, slugify
from utils.uploads import save_upload


@admin_bp.route("/social", methods=["GET", "POST"])
@admin_required
def social_links():
    if request.method == "POST":
        for link in SocialLink.query.all():
            link.url = request.form.get(f"url_{link.platform}", link.url)
            link.is_active = f"active_{link.platform}" in request.form
        db.session.commit()
        flash("Social links updated.", "success")
        return redirect(url_for("admin.social_links"))
    links = SocialLink.query.order_by(SocialLink.sort_order).all()
    return render_template("admin/social.html", links=links)


@admin_bp.route("/services/category/<int:cid>/delete", methods=["POST"])
@admin_required
def delete_category(cid):
    cat = ServiceCategory.query.get_or_404(cid)
    db.session.delete(cat)
    db.session.commit()
    flash("Service category deleted.", "success")
    return redirect(url_for("admin.services"))


@admin_bp.route("/services/category/<int:cid>/move/<direction>", methods=["POST"])
@admin_required
def move_category(cid, direction):
    cat = ServiceCategory.query.get_or_404(cid)
    siblings = (
        ServiceCategory.query.filter_by(service_group=cat.service_group)
        .order_by(ServiceCategory.sort_order)
        .all()
    )
    ids = [c.id for c in siblings]
    if cid in ids:
        idx = ids.index(cid)
        swap_idx = idx - 1 if direction == "up" and idx > 0 else idx + 1 if direction == "down" and idx < len(ids) - 1 else idx
        if swap_idx != idx:
            siblings[idx].sort_order, siblings[swap_idx].sort_order = siblings[swap_idx].sort_order, siblings[idx].sort_order
            db.session.commit()
    return redirect(url_for("admin.services"))


@admin_bp.route("/services/item/<int:iid>/edit", methods=["POST"])
@admin_required
def edit_service_item(iid):
    item = ServiceItem.query.get_or_404(iid)
    item.name = request.form.get("name", item.name).strip() or item.name
    item.is_active = "is_active" in request.form
    db.session.commit()
    return redirect(url_for("admin.edit_category", cid=item.category_id))


@admin_bp.route("/services/item/<int:iid>/move/<direction>", methods=["POST"])
@admin_required
def move_service_item(iid, direction):
    item = ServiceItem.query.get_or_404(iid)
    siblings = ServiceItem.query.filter_by(category_id=item.category_id).order_by(ServiceItem.sort_order).all()
    ids = [i.id for i in siblings]
    idx = ids.index(iid)
    swap_idx = idx - 1 if direction == "up" and idx > 0 else idx + 1 if direction == "down" and idx < len(ids) - 1 else idx
    if swap_idx != idx:
        siblings[idx].sort_order, siblings[swap_idx].sort_order = siblings[swap_idx].sort_order, siblings[idx].sort_order
        db.session.commit()
    return redirect(url_for("admin.edit_category", cid=item.category_id))


@admin_bp.route("/products/add", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        slug = slugify(request.form.get("slug") or name)
        if not name:
            flash("Product name is required.", "error")
            return redirect(url_for("admin.add_product"))
        max_order = db.session.query(db.func.max(Product.sort_order)).scalar() or 0
        product = Product(
            slug=slug,
            name=name,
            tagline=request.form.get("tagline", ""),
            short_description=request.form.get("short_description", ""),
            description=request.form.get("description", ""),
            cta_text=request.form.get("cta_text", "Try it"),
            cta_url=request.form.get("cta_url", ""),
            sort_order=max_order + 1,
            is_active="is_active" in request.form,
        )
        if "image" in request.files:
            product.image_filename = save_upload(request.files["image"], "product")
        db.session.add(product)
        db.session.commit()
        flash("Product created.", "success")
        return redirect(url_for("admin.edit_product", pid=product.id))
    return render_template("admin/add_product.html")


@admin_bp.route("/products/<int:pid>/delete", methods=["POST"])
@admin_required
def delete_product(pid):
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/products/<int:pid>/move/<direction>", methods=["POST"])
@admin_required
def move_product(pid, direction):
    products = Product.query.order_by(Product.sort_order).all()
    ids = [p.id for p in products]
    if pid not in ids:
        return redirect(url_for("admin.products"))
    idx = ids.index(pid)
    swap_idx = idx - 1 if direction == "up" and idx > 0 else idx + 1 if direction == "down" and idx < len(ids) - 1 else idx
    if swap_idx != idx:
        products[idx].sort_order, products[swap_idx].sort_order = products[swap_idx].sort_order, products[idx].sort_order
        db.session.commit()
    return redirect(url_for("admin.products"))


@admin_bp.route("/products/<int:pid>/feature", methods=["POST"])
@admin_required
def add_product_feature(pid):
    text = request.form.get("text", "").strip()
    if text:
        max_order = db.session.query(db.func.max(ProductFeature.sort_order)).filter_by(product_id=pid).scalar() or 0
        db.session.add(ProductFeature(product_id=pid, text=text, sort_order=max_order + 1))
        db.session.commit()
    return redirect(url_for("admin.edit_product", pid=pid))


@admin_bp.route("/products/feature/<int:fid>/delete", methods=["POST"])
@admin_required
def delete_product_feature(fid):
    feature = ProductFeature.query.get_or_404(fid)
    pid = feature.product_id
    db.session.delete(feature)
    db.session.commit()
    return redirect(url_for("admin.edit_product", pid=pid))


@admin_bp.route("/learning/<int:lid>", methods=["GET", "POST"])
@admin_required
def edit_learning(lid):
    program = LearningService.query.get_or_404(lid)
    if request.method == "POST":
        program.title = request.form.get("title", program.title)
        program.description = request.form.get("description", "")
        program.cta_text = request.form.get("cta_text", "Learn More")
        program.cta_url = request.form.get("cta_url", "")
        program.is_active = "is_active" in request.form
        if "image" in request.files and request.files["image"].filename:
            program.image_filename = save_upload(request.files["image"], "learning")
        db.session.commit()
        flash("Learning program updated.", "success")
        return redirect(url_for("admin.edit_learning", lid=lid))
    return render_template("admin/edit_learning.html", program=program)


@admin_bp.route("/learning/<int:lid>/delete", methods=["POST"])
@admin_required
def delete_learning(lid):
    program = LearningService.query.get_or_404(lid)
    db.session.delete(program)
    db.session.commit()
    flash("Learning program deleted.", "success")
    return redirect(url_for("admin.learning"))


@admin_bp.route("/learning/<int:lid>/move/<direction>", methods=["POST"])
@admin_required
def move_learning(lid, direction):
    programs = LearningService.query.order_by(LearningService.sort_order).all()
    ids = [p.id for p in programs]
    idx = ids.index(lid)
    swap_idx = idx - 1 if direction == "up" and idx > 0 else idx + 1 if direction == "down" and idx < len(ids) - 1 else idx
    if swap_idx != idx:
        programs[idx].sort_order, programs[swap_idx].sort_order = programs[swap_idx].sort_order, programs[idx].sort_order
        db.session.commit()
    return redirect(url_for("admin.learning"))


@admin_bp.route("/blogs/<int:bid>/delete", methods=["POST"])
@admin_required
def delete_blog(bid):
    post = BlogPost.query.get_or_404(bid)
    db.session.delete(post)
    db.session.commit()
    flash("Blog post deleted.", "success")
    return redirect(url_for("admin.blogs"))


@admin_bp.route("/blogs/<int:bid>/move/<direction>", methods=["POST"])
@admin_required
def move_blog(bid, direction):
    posts = BlogPost.query.order_by(BlogPost.sort_order).all()
    ids = [p.id for p in posts]
    if bid not in ids:
        return redirect(url_for("admin.blogs"))
    idx = ids.index(bid)
    swap_idx = idx - 1 if direction == "up" and idx > 0 else idx + 1 if direction == "down" and idx < len(ids) - 1 else idx
    if swap_idx != idx:
        posts[idx].sort_order, posts[swap_idx].sort_order = posts[swap_idx].sort_order, posts[idx].sort_order
        db.session.commit()
    return redirect(url_for("admin.blogs"))


@admin_bp.route("/why/<int:wid>/toggle", methods=["POST"])
@admin_required
def toggle_why(wid):
    item = WhyChooseItem.query.get_or_404(wid)
    item.is_active = not item.is_active
    db.session.commit()
    return redirect(url_for("admin.about"))


@admin_bp.route("/why/<int:wid>/delete", methods=["POST"])
@admin_required
def delete_why(wid):
    item = WhyChooseItem.query.get_or_404(wid)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("admin.about"))
