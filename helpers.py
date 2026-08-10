from models import Product, ServiceCategory, SocialLink


SOCIAL_PLATFORMS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("youtube", "YouTube"),
    ("linkedin", "LinkedIn"),
    ("x", "X (Twitter)"),
    ("threads", "Threads"),
]


def active_social_links():
    return (
        SocialLink.query.filter_by(is_active=True)
        .order_by(SocialLink.sort_order)
        .all()
    )


def consultation_service_options():
    """Build dropdown options from active service categories and items."""
    options = []
    categories = (
        ServiceCategory.query.filter_by(is_active=True)
        .order_by(ServiceCategory.service_group, ServiceCategory.sort_order)
        .all()
    )
    for cat in categories:
        options.append({"value": cat.title, "label": cat.title, "group": cat.service_group})
        for item in cat.items:
            if getattr(item, "is_active", True):
                label = f"{cat.title} — {item.name}"
                options.append({"value": label, "label": label, "group": cat.service_group})
    return options


def grouped_services():
    tech = (
        ServiceCategory.query.filter_by(is_active=True, service_group="technology")
        .order_by(ServiceCategory.sort_order)
        .all()
    )
    marketing = (
        ServiceCategory.query.filter_by(is_active=True, service_group="digital_marketing")
        .order_by(ServiceCategory.sort_order)
        .all()
    )
    return tech, marketing


def suggestion_form_options():
    """Products and services for the suggestion form checkboxes."""
    products = Product.query.filter_by(is_active=True).order_by(Product.sort_order).all()
    tech_categories, marketing_categories = grouped_services()
    service_groups = [
        ("Technology Services", tech_categories),
        ("Digital Marketing Services", marketing_categories),
    ]
    return products, service_groups


def format_offerings(offerings):
    """Turn prefixed offering values into readable labels for storage."""
    labels = []
    for offering in offerings:
        if offering.startswith("p:"):
            labels.append(offering[2:])
        elif offering.startswith("s:"):
            labels.append(offering[2:])
        elif offering.startswith("other:"):
            labels.append(offering[6:])
        else:
            labels.append(offering)
    return ", ".join(labels)
