"""Seed initial content from the Rajaro website design PDF."""

from datetime import date

from models import (
    AffiliateBenefit,
    AffiliateStep,
    BlogPost,
    ClientLogo,
    HeroPromise,
    JobPosting,
    LearningService,
    Product,
    ProductFeature,
    ProductPricingRow,
    ProductPricingSection,
    ServiceCategory,
    ServiceItem,
    SiteContent,
    SocialLink,
    WhyChooseItem,
    db,
)


def get_content(key, default=""):
    row = SiteContent.query.filter_by(key=key).first()
    return row.value if row else default


def set_content(key, value):
    row = SiteContent.query.filter_by(key=key).first()
    if row:
        row.value = value
    else:
        db.session.add(SiteContent(key=key, value=value))


def seed_database():
    if SiteContent.query.first():
        return

    defaults = {
        "site_name": "Rajaro Solutions Private Limited",
        "hero_title": "I am Rajaro",
        "hero_subtitle": "From India for the world",
        "hero_intro": (
            "Technology is the driving force behind modern business success. "
            "At Rajaro Solutions Private Limited, we help startups, SMEs, enterprises, "
            "government organizations, and global businesses transform ideas into "
            "innovative digital solutions."
        ),
        "services_intro": (
            "Our expertise spans software engineering, artificial intelligence, cloud computing, "
            "cybersecurity, enterprise platforms, blockchain, managed IT services, and digital "
            "marketing. By combining technology, strategy, creativity, and industry expertise, "
            "we deliver scalable, secure, and future-ready solutions."
        ),
        "about_what_we_do": (
            "Rajaro Solutions Private Limited is a technology, innovation, and digital transformation "
            "company focused on building world-class software, intelligent platforms, and "
            "industry-specific digital ecosystems. We partner with startups, SMEs, enterprises, government "
            "organizations, and global businesses to create scalable technology solutions while also "
            "developing innovative products that solve real-world challenges across multiple industries. "
            "With expertise in software engineering, artificial intelligence, cloud computing, cybersecurity, "
            "blockchain, enterprise platforms, digital marketing, and emerging technologies, we are committed "
            "to shaping the future through continuous innovation and sustainable growth. We design, develop, "
            "and manage innovative technology solutions that help businesses transform digitally and grow "
            "efficiently. Beyond providing technology and digital marketing services, we continuously research, "
            "build, launch, and operate proprietary platforms and digital ecosystems across multiple industries, "
            "creating long-term value for businesses, consumers, and communities."
        ),
        "about_who_we_are": (
            "We are a team of technology experts, innovators, designers, engineers, digital marketers, "
            "and business strategists passionate about solving real-world challenges through digital innovation. "
            "By combining creativity, technical excellence, and industry expertise, we deliver future-ready "
            "software, scalable platforms, innovative digital products, and data-driven marketing solutions "
            "that drive measurable business success."
        ),
        "mission": (
            "To empower businesses and communities by delivering innovative technology solutions "
            "that simplify operations, accelerate growth, create new digital opportunities, and drive "
            "sustainable success through innovation, trust, and excellence."
        ),
        "vision": (
            "To become a globally trusted and recognized technology leader, building transformative "
            "platforms, future-ready digital products, and connected ecosystems that redefine "
            "industries and improve lives."
        ),
        "about_founder": "About Founder — content editable from admin panel.",
        "affiliate_headline": "Earn 10% Fixed commission from every customer you refer. It's free to join.",
        "affiliate_cta": "Become a Rajaro Affiliate",
        "affiliate_email": "partners@rajaro.com",
        "contact_address": "Erode, Tamil Nadu 638004, India",
        "contact_phone": "8110011588",
        "contact_email": "contact@rajaro.com",
        "contact_hours": "Monday to Friday — 10:00 AM IST to 6:00 PM IST",
        "learning_headline": "Learn, Connect & Grow",
        "learning_intro": (
            "Empower your personal and professional growth through our comprehensive learning ecosystem. "
            "We offer expertly designed Courses, insightful Webinars, and engaging Events."
        ),
        "social_facebook": "#",
        "social_twitter": "#",
        "social_linkedin": "#",
        "social_instagram": "#",
        "consultation_headline": "Ready to Transform Your Business?",
        "consultation_text": (
            "Whether you're building a new digital product, modernizing existing systems, adopting AI, "
            "strengthening cybersecurity, migrating to the cloud, or scaling your digital marketing efforts, "
            "Rajaro Solutions Private Limited is your trusted technology and business transformation partner."
        ),
    }
    for key, value in defaults.items():
        set_content(key, value)

    promises = [
        "I promise to serve and solve my problems of my customer",
        "I promise to offer best products to my customer",
        "I promise that today I will be better than yesterday",
    ]
    for i, text in enumerate(promises):
        db.session.add(HeroPromise(text=text, sort_order=i))

    categories_data = [
        {
            "title": "Digital Engineering Services",
            "subtitle": "Build Innovative Digital Products That Drive Business Growth",
            "description": "We design, develop, modernize, and maintain secure, scalable, and high-performance software solutions.",
            "items": [
                "Custom Software Development", "Full Stack Web Development",
                "Mobile App Development (Android & iOS)", "Backend Development & API Integration",
                "UI/UX Design", "Gen AI - UI UX", "Frontend Development",
                "Enterprise Application Development", "Software Architecture & System Design",
                "DevSecOps Implementation", "CI/CD Pipeline Automation", "Hyperautomation Solutions",
                "Site Reliability Engineering (SRE)", "Chaos Engineering",
                "Application Modernization", "Application Support & Maintenance",
            ],
        },
        {
            "title": "Artificial Intelligence & Data Analytics",
            "subtitle": "Turn Data into Intelligent Business Decisions",
            "description": "Unlock the full value of your business data through AI-powered analytics, automation, and predictive intelligence.",
            "items": [
                "Artificial Intelligence Solutions", "Machine Learning", "Generative AI Integration",
                "AI Chatbots & Virtual Assistants", "Data Analytics", "Business Intelligence Dashboards",
                "Data Visualization", "Predictive Analytics", "Data Science", "Big Data Engineering",
                "Data Warehousing", "Data Lakes", "Data Fabric", "IoT Analytics",
                "KPI Reporting & Business Insights",
            ],
        },
        {
            "title": "Cloud & Infrastructure Services",
            "subtitle": "Build a Secure, Scalable and Cost-Optimized Cloud Environment",
            "description": "Accelerate digital transformation through cloud migration, modernization, infrastructure optimization, and managed cloud operations.",
            "items": [
                "Cloud Strategy & Consulting", "Cloud Migration", "Multi-Cloud Solutions",
                "Hybrid Cloud Deployment", "Cloud Infrastructure Management", "Platform Engineering",
                "Cloud Security", "Cloud Cost Optimization (FinOps)", "Disaster Recovery",
                "Backup Solutions", "Mainframe Modernization", "SAP on Cloud",
                "Cloud Monitoring", "Managed Cloud Services",
            ],
        },
        {
            "title": "Cybersecurity Services",
            "subtitle": "Protect Your Business Against Evolving Cyber Threats",
            "description": "Our cybersecurity experts help organizations secure applications, infrastructure, networks, and cloud environments.",
            "items": [
                "Cybersecurity Consulting", "Security Assessment", "Vulnerability Assessment",
                "Penetration Testing", "Security Operations Center (SOC)", "SIEM Solutions",
                "Identity & Access Management (IAM)", "Customer Identity Management (CIAM)",
                "Zero Trust Security", "Cloud Security", "Threat Detection & Incident Response",
                "Governance, Risk & Compliance (GRC)", "Security Engineering", "Security Monitoring",
            ],
        },
        {
            "title": "Blockchain & Web3 Solutions",
            "subtitle": "Secure, Transparent and Decentralized Digital Innovation",
            "description": "We build blockchain-powered applications that enhance transparency, security, automation, and digital ownership.",
            "items": [
                "Blockchain Consulting", "Smart Contract Development", "Ethereum Development",
                "Hyperledger Solutions", "Private & Public Blockchain", "Web3 Development",
                "Decentralized Applications (dApps)", "NFT Marketplace Development",
                "Tokenization Platforms", "Digital Asset Management", "IPFS Integration",
                "Blockchain Security Audits",
            ],
        },
        {
            "title": "Quality Assurance & Testing",
            "subtitle": "Deliver Reliable Software with Superior Quality",
            "description": "Our QA specialists ensure every application meets the highest standards of quality, security, performance, and reliability.",
            "items": [
                "QA Strategy", "Manual Testing", "Automation Testing", "Functional Testing",
                "Regression Testing", "Performance Testing", "Security Testing", "API Testing",
                "Mobile Testing", "Agile Testing", "Test Automation Frameworks",
                "Independent Software Validation", "Managed Testing Services",
            ],
        },
        {
            "title": "Digital Marketing Services",
            "subtitle": "Grow Your Business Through Data-Driven Digital Marketing",
            "description": "We combine strategy, creativity, technology, and analytics to help businesses build powerful brands and achieve measurable growth.",
            "items": [
                "Search Engine Optimization (SEO)", "Content Marketing", "Social Media Marketing",
                "Social Media Management", "Performance Marketing", "Pay-Per-Click (PPC) Advertising",
                "Email Marketing", "Branding & Brand Strategy", "WhatsApp Business Solutions",
                "Influencer Marketing & Personal Branding", "Video Production & Digital PR",
                "Online Reputation Management", "Marketing Automation",
                "Marketing Analytics & Business Intelligence", "Lead Generation Services",
                "Business Growth Consulting & Mentorship",
            ],
        },
        {
            "title": "Enterprise Business Solutions",
            "subtitle": "Modern Enterprise Platforms That Improve Business Performance",
            "description": "We implement enterprise platforms that streamline operations, automate workflows, and improve collaboration.",
            "items": [
                "SAP Solutions", "Salesforce Solutions", "Oracle Solutions", "Microsoft Dynamics 365",
                "ServiceNow Solutions", "Workday Solutions", "Adobe Experience Cloud",
                "Sitecore Development", "ERP Consulting", "CRM Implementation",
                "Enterprise Application Integration", "Digital Workflow Automation",
                "SaaS Platform Management", "Enterprise Support Services",
            ],
        },
        {
            "title": "Managed IT Services",
            "subtitle": "Reliable IT Operations for Maximum Business Continuity",
            "description": "Focus on growing your business while our experts manage your IT infrastructure, applications, security, and support.",
            "items": [
                "Infrastructure Management", "Cloud Operations", "Server Administration",
                "Network Monitoring", "Database Administration", "Application Management",
                "Security Monitoring", "Managed Security Services", "Backup & Disaster Recovery",
                "Remote IT Support", "Help Desk Services", "Performance Optimization",
                "Preventive Maintenance", "IT Operations Management",
            ],
        },
    ]

    for ci, cat in enumerate(categories_data):
        group = "digital_marketing" if "Digital Marketing" in cat["title"] else "technology"
        category = ServiceCategory(
            title=cat["title"],
            subtitle=cat["subtitle"],
            description=cat["description"],
            service_group=group,
            sort_order=ci,
        )
        db.session.add(category)
        db.session.flush()
        for si, item_name in enumerate(cat["items"]):
            db.session.add(ServiceItem(category_id=category.id, name=item_name, sort_order=si))

    subitra = Product(
        slug="subitra",
        name="Subitra",
        tagline="Everything You Need, All in One App",
        description=(
            "Subitra is a next-generation hyperlocal super app designed to simplify everyday life "
            "by connecting local business and sellers with their customers, delivery partners, "
            "logistics providers, and sustainable recycling services through one intelligent digital platform. "
            "We provide digital platform to sellers, local business and their customers whether they can order "
            "instant delivery within minutes for nearby store, same-day or scheduled deliveries across your city, "
            "domestic logistics across India, or international shipping, Subitra provides flexible delivery "
            "solutions for every requirement. You can also send parcels and documents, schedule doorstep scrap "
            "collection to earn Eco Rewards, discover nearby businesses based on your location, and access a wide "
            "range of trusted services—all from a single application. Promoting responsible recycling through "
            "doorstep scrap collecting pickup for recyclable materials and earn eco-rewards that value for scrap "
            "material while contributing to a cleaner and greener environment. Reward points earned through scrap "
            "materials can be redeemed for discounts, offers, and future purchases or even withdrawn to bank account."
        ),
        cta_text="Try it",
        cta_url="https://subitra.com/",
        sort_order=0,
    )
    db.session.add(subitra)
    db.session.flush()

    customer_section = ProductPricingSection(product_id=subitra.id, title="Customer Pricing", sort_order=0)
    db.session.add(customer_section)
    db.session.flush()
    for i, (svc, price) in enumerate([
        ("App Registration", "Free"),
        ("Delivery", "Delivery fee based on distance"),
        ("Courier Service", "Based on parcel size & distance"),
        ("Scrap Collection", "Free pickup (eligible locations)"),
    ]):
        db.session.add(ProductPricingRow(section_id=customer_section.id, service_name=svc, price=price, sort_order=i))

    business_section = ProductPricingSection(product_id=subitra.id, title="Business Pricing", sort_order=1)
    db.session.add(business_section)
    db.session.flush()
    for i, (svc, price) in enumerate([
        ("Seller Subscription — Monthly Plan", "₹1,999 / Seller"),
        ("Seller Subscription — Annual Plan", "₹21,999 / Seller"),
    ]):
        db.session.add(ProductPricingRow(section_id=business_section.id, service_name=svc, price=price, sort_order=i))

    rajarorise = Product(
        slug="rajarorise",
        name="RajaroRise",
        tagline="Comprehensive Fundraising and Capital Raising Marketplace",
        description=(
            "RajaroRise is a comprehensive fundraising and capital raising marketplace designed to connect "
            "startups, businesses, investors, lenders, NGOs, and event organizers through one secure digital platform. "
            "Whether you're raising capital, seeking investment opportunities, selling business equity, or managing "
            "fundraising campaigns, RajaroRise provides the tools and professional support to help you succeed. "
            "As a technology-enabled facilitator, RajaroRise streamlines fundraising while ensuring transparency, "
            "efficiency, and seamless collaboration between fundraisers and investors. Funds are exchanged directly "
            "between participating parties based on mutually agreed terms, while RajaroRise provides the platform, "
            "campaign management tools, advisory services, and transaction support."
        ),
        cta_text="Try it",
        cta_url="https://rajarorise.com/",
        sort_order=1,
    )
    db.session.add(rajarorise)
    db.session.flush()

    fundraiser = ProductPricingSection(product_id=rajarorise.id, title="Fundraiser — Service Charges", sort_order=0)
    db.session.add(fundraiser)
    db.session.flush()
    for i, (svc, price) in enumerate([
        ("Equity/Secondary market campaign Setup Fee", "₹3,000"),
        ("Equity Success Fee", "0%–9%"),
        ("Debt/Revenue Success Fee", "0%–9%"),
        ("Reward Campaign Success Fee", "0%–9%"),
        ("Secondary Market Success Fee", "0%–9%"),
        ("Event Ticket Platform Fee", "0%–5%"),
        ("Advanced Campaign Features", "Additional 0%–3%"),
    ]):
        db.session.add(ProductPricingRow(section_id=fundraiser.id, service_name=svc, price=price, sort_order=i))

    investor = ProductPricingSection(product_id=rajarorise.id, title="Investor/Donators — Service Charges", sort_order=1)
    db.session.add(investor)
    db.session.flush()
    for i, (svc, price) in enumerate([
        ("Equity/Secondary marker Annual Subscription", "₹20,000"),
        ("Equity/Secondary marker Per Deal Access", "₹3,000"),
        ("Reward/Donators campaign access", "Completely free"),
    ]):
        db.session.add(ProductPricingRow(section_id=investor.id, service_name=svc, price=price, sort_order=i))

    debt_recovery = ProductPricingSection(
        product_id=rajarorise.id, title="Debt Recovery Services (Where Applicable)", sort_order=2
    )
    db.session.add(debt_recovery)
    db.session.flush()
    for i, (svc, price) in enumerate([
        ("Facilitation Fee", "0%–5%"),
        ("Collection Fee", "0%–5%"),
        ("Recovery Fee", "Up to 100% of the recovered amount, subject to contractual terms and applicable laws"),
        ("Late Payment Charges", "Applicable late payment charges may be imposed on overdue repayments"),
        ("Payment Processing", "Securely processed through trusted third-party payment service providers"),
    ]):
        db.session.add(ProductPricingRow(section_id=debt_recovery.id, service_name=svc, price=price, sort_order=i))

    for name in ["Warner & Spencer", "Hanover and Tyke", "Studio Shodwe", "Rimberio"]:
        db.session.add(ClientLogo(name=name))

    why_items = [
        "End-to-End Technology & Marketing Partner",
        "Experienced Team of Industry Professionals",
        "AI-Driven and Future-Ready Solutions",
        "Scalable Enterprise Architecture",
        "Security-First Development Approach",
        "Agile Delivery Methodology",
        "Transparent Communication",
        "Cost-Effective Engagement Models",
        "Dedicated Post-Launch Support",
        "Customized Solutions for Every Business",
    ]
    for i, text in enumerate(why_items):
        db.session.add(WhyChooseItem(text=text, sort_order=i))

    learning = [
        ("Courses", "Structured online and offline programs designed to build practical skills and industry knowledge."),
        ("Webinars", "Live expert-led sessions covering emerging trends, technologies, business strategies, and professional development."),
        ("Events", "Conferences, workshops, networking meetups, seminars, product launches, and industry events."),
    ]
    for i, (title, desc) in enumerate(learning):
        db.session.add(LearningService(title=title, description=desc, sort_order=i))

    steps = [
        (1, "Join the program", "Become a Rajaro affiliate. Get access to exclusive affiliate portal once approved after 24hrs of form submission."),
        (2, "Promote the products", "Share your unique affiliate links via blogs, social media posts, email newsletters, videos and other digital forums."),
        (3, "Earn commissions", "Earn a share of the revenue for every qualified sale after trial period via your links for the lifetime."),
        (4, "Monthly bank payouts", "Direct bank transfer every month. No threshold, no waiting period, no surprises."),
    ]
    for i, (num, title, desc) in enumerate(steps):
        db.session.add(AffiliateStep(step_number=num, title=title, description=desc, sort_order=i))

    benefits = [
        ("Dedicated partner manager", "A real human who knows your pipeline. On call, on WhatsApp, with fast turnaround and co-pitch & demo support."),
        ("Support & Transparency", "Access a full resource center, track performance with customizable reports, and lean on the Affiliate team."),
        ("Growth Opportunities", "Grow within the program by leveling up. The more customers you refer, the more you earn."),
    ]
    for i, (title, desc) in enumerate(benefits):
        db.session.add(AffiliateBenefit(title=title, description=desc, sort_order=i))

    job = JobPosting(
        title="Frontend Web Developer - HTML, CSS (Remote)",
        mode="Remote (Work from Anywhere), Field, office, on-site, hybrid, Internship",
        job_type="contract, Full time, Part time, temporary, volunteer, internship, other",
        shift="any, day, night",
        location="Erode, Tamil Nadu, India",
        openings=4,
        income="$30 - $80/hour, Performance based stipend up-to 7500.00/-",
        skills="Domain->Sales->Sales Planning",
        reference_code="Rajaro-Career-0001",
        expiry_date=date(2026, 12, 1),
        education="Graduate",
        gender="Any",
        short_description="Frontend Developer role building responsive user interfaces using HTML and CSS.",
        description=(
            "Role Overview:\nWe are hiring for one of our clients, seeking a Frontend Developer to work on a contract basis.\n\n"
            "Key Responsibilities:\n• Develop and maintain front-end components using HTML, CSS\n"
            "• Ensure cross-browser compatibility and responsive design\n"
            "• Collaborate with design teams to implement pixel-perfect UI elements\n\n"
            "Required Skills:\n• Proficiency in HTML and CSS\n• Responsive design principles\n"
            "• Familiarity with CSS preprocessors or frameworks\n• Ability to implement designs from Figma or Sketch"
        ),
        is_active=True,
    )
    db.session.add(job)

    blog = BlogPost(
        title="Why Employers Should Stop Chasing Perfect Candidates and Start Building Flexible Workforce Strategies",
        slug="flexible-workforce-strategies",
        excerpt="Building flexible workforce strategies for modern hiring challenges.",
        content=(
            "In the U.S., almost everyone depends on their car for daily life. Indeed, 91% of households own at least one, "
            "making cars a key part of our routines.\n\n"
            "But change is coming fast; electric vehicles (EVs) are gaining ground over gasoline-powered cars.\n\n"
            "## Where the EV Industry Needs Talent the Most\n\n"
            "1. Software Engineers\n2. Battery Manufacturing Experts\n\n"
            "## Charging Ahead: How to Win the EV Talent Race\n\n"
            "Winning with Reliable Partnerships: Grab Your Share of the EV Market."
        ),
        published_at=date(2026, 6, 11),
        is_published=True,
    )
    db.session.add(blog)

    blog2 = BlogPost(
        title="Charge Ahead in the EV Market with Expert Teams",
        slug="ev-market-expert-teams",
        excerpt="Demand for software engineers in the EV sector is rising.",
        content="While demand for software engineers in the EV sector is rising, there's a shortage of professionals with automotive experience.",
        published_at=date(2024, 11, 15),
        is_published=True,
    )
    db.session.add(blog2)

    db.session.commit()


def patch_database():
    """Apply design PDF fixes to an existing database."""
    patches = {
        "contact_email": "contact@rajaro.com",
        "contact_hours": "Monday to Friday — 10:00 AM IST to 6:00 PM IST",
        "about_what_we_do": (
            "Rajaro Solutions Private Limited is a technology, innovation, and digital transformation "
            "company focused on building world-class software, intelligent platforms, and "
            "industry-specific digital ecosystems. We partner with startups, SMEs, enterprises, government "
            "organizations, and global businesses to create scalable technology solutions while also "
            "developing innovative products that solve real-world challenges across multiple industries. "
            "With expertise in software engineering, artificial intelligence, cloud computing, cybersecurity, "
            "blockchain, enterprise platforms, digital marketing, and emerging technologies, we are committed "
            "to shaping the future through continuous innovation and sustainable growth. We design, develop, "
            "and manage innovative technology solutions that help businesses transform digitally and grow "
            "efficiently. Beyond providing technology and digital marketing services, we continuously research, "
            "build, launch, and operate proprietary platforms and digital ecosystems across multiple industries, "
            "creating long-term value for businesses, consumers, and communities."
        ),
        "about_who_we_are": (
            "We are a team of technology experts, innovators, designers, engineers, digital marketers, "
            "and business strategists passionate about solving real-world challenges through digital innovation. "
            "By combining creativity, technical excellence, and industry expertise, we deliver future-ready "
            "software, scalable platforms, innovative digital products, and data-driven marketing solutions "
            "that drive measurable business success."
        ),
    }
    for key, value in patches.items():
        set_content(key, value)

    subitra = Product.query.filter_by(slug="subitra").first()
    if subitra:
        subitra.description = (
            "Subitra is a next-generation hyperlocal super app designed to simplify everyday life "
            "by connecting local business and sellers with their customers, delivery partners, "
            "logistics providers, and sustainable recycling services through one intelligent digital platform. "
            "We provide digital platform to sellers, local business and their customers whether they can order "
            "instant delivery within minutes for nearby store, same-day or scheduled deliveries across your city, "
            "domestic logistics across India, or international shipping, Subitra provides flexible delivery "
            "solutions for every requirement. You can also send parcels and documents, schedule doorstep scrap "
            "collection to earn Eco Rewards, discover nearby businesses based on your location, and access a wide "
            "range of trusted services—all from a single application. Promoting responsible recycling through "
            "doorstep scrap collecting pickup for recyclable materials and earn eco-rewards that value for scrap "
            "material while contributing to a cleaner and greener environment. Reward points earned through scrap "
            "materials can be redeemed for discounts, offers, and future purchases or even withdrawn to bank account."
        )
        subitra.cta_url = "https://subitra.com/"

    rajarorise = Product.query.filter_by(slug="rajarorise").first()
    if rajarorise:
        rajarorise.description = (
            "RajaroRise is a comprehensive fundraising and capital raising marketplace designed to connect "
            "startups, businesses, investors, lenders, NGOs, and event organizers through one secure digital platform. "
            "Whether you're raising capital, seeking investment opportunities, selling business equity, or managing "
            "fundraising campaigns, RajaroRise provides the tools and professional support to help you succeed. "
            "As a technology-enabled facilitator, RajaroRise streamlines fundraising while ensuring transparency, "
            "efficiency, and seamless collaboration between fundraisers and investors. Funds are exchanged directly "
            "between participating parties based on mutually agreed terms, while RajaroRise provides the platform, "
            "campaign management tools, advisory services, and transaction support."
        )
        rajarorise.cta_url = "https://rajarorise.com/"

        if not ProductPricingSection.query.filter_by(
            product_id=rajarorise.id, title="Debt Recovery Services (Where Applicable)"
        ).first():
            debt_recovery = ProductPricingSection(
                product_id=rajarorise.id, title="Debt Recovery Services (Where Applicable)", sort_order=2
            )
            db.session.add(debt_recovery)
            db.session.flush()
            for i, (svc, price) in enumerate([
                ("Facilitation Fee", "0%–5%"),
                ("Collection Fee", "0%–5%"),
                ("Recovery Fee", "Up to 100% of the recovered amount, subject to contractual terms and applicable laws"),
                ("Late Payment Charges", "Applicable late payment charges may be imposed on overdue repayments"),
                ("Payment Processing", "Securely processed through trusted third-party payment service providers"),
            ]):
                db.session.add(
                    ProductPricingRow(section_id=debt_recovery.id, service_name=svc, price=price, sort_order=i)
                )

    _seed_social_links()
    _patch_service_groups()
    _patch_product_short_descriptions()

    db.session.commit()


def _seed_social_links():
    defaults = [
        ("facebook", "Facebook", 0),
        ("instagram", "Instagram", 1),
        ("youtube", "YouTube", 2),
        ("linkedin", "LinkedIn", 3),
        ("x", "X (Twitter)", 4),
        ("threads", "Threads", 5),
    ]
    legacy = {
        "facebook": get_content("social_facebook", "#"),
        "instagram": get_content("social_instagram", "#"),
        "linkedin": get_content("social_linkedin", "#"),
        "x": get_content("social_twitter", "#"),
    }
    for platform, label, order in defaults:
        if not SocialLink.query.filter_by(platform=platform).first():
            db.session.add(
                SocialLink(
                    platform=platform,
                    label=label,
                    url=legacy.get(platform, "#"),
                    sort_order=order,
                    is_active=True,
                )
            )


def _patch_service_groups():
    for cat in ServiceCategory.query.all():
        if "Digital Marketing" in cat.title:
            cat.service_group = "digital_marketing"
        elif not cat.service_group:
            cat.service_group = "technology"


def _patch_product_short_descriptions():
    for product in Product.query.all():
        if not product.short_description and product.description:
            product.short_description = product.description[:220]
