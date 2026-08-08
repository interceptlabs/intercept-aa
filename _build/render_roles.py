#!/usr/bin/env python3
"""Renders the 9 job/role detail pages under careers/open-roles/<slug>/.

Source: wireframes at ~/Downloads/New Wire Frames/pages/roles/*.html — one consistent
template (crumb / rhero / rbody sections / aiband / apply), but the exact section set
and "What you'll do" structure (h3-subhead-per-category vs. one flat ul with category
labels as plain <li>s) differs per role, so each role's content is transcribed here
verbatim rather than forced into one shape. No section is invented; sections not
present in a given source file (e.g. "Why Intercept") are simply omitted for that role.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import esc, head_html, header_html, footer_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- page CSS ----
# .ph / .eyebrow / .btn / .link already live in common.py — not redefined here.
# Sized/colored off the same tokens the careers hub + open-roles listing use
# (render_careers.py), for visual continuity across the careers page family.
# Sections are separated by spacing/bands, not rule lines, matching the rest
# of the site (see common.py's "bands carry emphasis, not lines" CSS comment).
CSS = """
.crumb{border-bottom:1px solid var(--line);background:var(--band)}
.crumb-row{max-width:var(--maxw);margin:0 auto;padding:11px 32px;font-size:var(--fs-8);color:var(--ink-3)}
.crumb-row b{color:var(--ink);font-weight:600}

.rhero{padding:48px 0 32px}
.rhero h1{font-size:var(--fs-1);line-height:1.04;letter-spacing:-.032em;margin:0 0 14px;max-width:20ch}
.rmeta{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 26px}
.rtag{font-size:var(--fs-8);font-weight:600;color:var(--ink-2);border:1px solid var(--line);padding:7px 14px;border-radius:999px}

.rbody{padding:8px 0 8px}
.rbody section{padding:34px 0}
.rbody h2{font-size:var(--fs-2);line-height:1.12;letter-spacing:-.026em;margin:0 0 18px;max-width:26ch}
.rbody h3{font-size:var(--fs-7);letter-spacing:.01em;margin:24px 0 10px;font-weight:700;color:var(--ink)}
.rbody h3:first-of-type{margin-top:0}
.rbody p{font-size:var(--fs-6);line-height:1.62;color:var(--ink-2);margin:0 0 14px;max-width:68ch}
.rbody ul{margin:0 0 8px;padding:0 0 0 20px;max-width:68ch}
.rbody li{font-size:var(--fs-6);line-height:1.58;color:var(--ink-2);margin:0 0 9px}

.aiband{background:var(--band);padding:44px 0;margin:8px 0}
.aiband h2{font-size:var(--fs-2);line-height:1.12;letter-spacing:-.026em;margin:0 0 14px;max-width:26ch}
.aiband .lede{font-size:var(--fs-6);color:var(--ink-2);margin:0 0 16px;max-width:60ch}
.aiband ul{margin:0;padding:0 0 0 20px;max-width:68ch}
.aiband li{font-size:var(--fs-6);line-height:1.58;color:var(--ink-2);margin:0 0 9px}

.apply{padding:52px 0}
.apply h2{font-size:var(--fs-2);line-height:1.08;letter-spacing:-.028em;margin:0 0 14px;max-width:22ch}
.apply p{font-size:var(--fs-6);color:var(--ink-2);margin:0 0 24px;max-width:56ch}
"""

# ---- shared, literally-identical-across-every-source-file copy ----
AI_INTRO = "Every role here works alongside AI teammates. This is what that looks like day to day."
APPLY_H2 = "Think this is you?"
APPLY_P = "Send us your resume and portfolio. We read every application, and only successful applicants are contacted for an interview."


def sec(title, blocks):
    """blocks: list of ('p', text) | ('h3', text) | ('ul', [items])"""
    parts = [f"<h2>{esc(title)}</h2>"]
    for kind, val in blocks:
        if kind == "p":
            parts.append(f"<p>{esc(val)}</p>")
        elif kind == "h3":
            parts.append(f"<h3>{esc(val)}</h3>")
        elif kind == "ul":
            parts.append("<ul>" + "".join(f"<li>{esc(i)}</li>" for i in val) + "</ul>")
    return "<section>" + "".join(parts) + "</section>"


def ul_html(items):
    return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


# ---- role data, transcribed verbatim from each wireframe source file ----
ROLES = [

    {
        "slug": "account-associate",
        "title": "Account Associate",
        "tag1": "Client leadership",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "We are looking for an Account Associate with prior coordination and/or administrative experience within an agency or fast-paced office setting (including internship). Ideal candidates will be solution-based team members with strong research and organization skills to manage various levels of agency support. They will contribute heavily to the deliverables of our Accounts Team to achieve the best results with B2B marketing programs and campaigns. APPLY TODAY to join our team."),
            ]),
            ("What you’ll do", [
                ("h3", "Client Interaction and Support"),
                ("ul", [
                    "Take detailed notes during client calls to capture key discussions, action items, and decisions.",
                    "Demonstrate initiative and proactivity in understanding client needs and addressing queries.",
                    "Provide prompt and professional email support to clients, addressing day-to-day inquiries and drafting correspondence as needed.",
                    "Expanding relationships with existing clients and vendors.",
                    "Understand client briefs thoroughly to effectively contribute to project planning and execution.",
                ]),
                ("h3", "Project Documentation and Quality Assurance"),
                ("ul", [
                    "Assist in the creation and maintenance of project documents, including internal briefs, client feedback reports, workback schedules and communication within the studio team.",
                    "Ensure accuracy and completeness of project documents through regular updates.",
                    "Conduct quality assurance checks on project assets to ensure they meet specified standards and requirements.",
                    "Provide an extra layer of quality assurance and review for agency work being submitted to clients for final approval or production",
                ]),
                ("h3", "Support to the Director, Accounts"),
                ("ul", [
                    "Act as a support to the Director, Accounts, across their different client teams (Pods), representing them in internal meetings they are not able to attend, and formalizing discussion points and decisions made",
                    "Take notes during internal briefing calls and all-hands status meetings, highlighting key points and action items.",
                    "Proactively contribute to discussions and offer insights to enhance team collaboration and efficiency.",
                    "Participate actively in internal brief calls, providing input and clarifications as needed.",
                    "Prepare materials and contribute to the delivery of internal account all-hands meetings, fostering a culture of transparency and teamwork.",
                ]),
                ("h3", "Project Management"),
                ("ul", [
                    "Utilize project management tools to maintain project tasks, assign responsibilities, and track progress.",
                    "Actively monitor and oversee the agency’s project management tool to ensure client projects are on-schedule and meeting proposed timelines.",
                    "Managing communications and deliverables with third-party vendors and partners based on program budgets, deadlines, and expectations.",
                    "Maintain workback schedules for project deliverables and timelines, ensuring adherence to deadlines.",
                    "Effectively manage workload and communicate any potential bandwidth issues to ensure timely delivery of projects.",
                    "Clearly understand project requirements and communicate them effectively to the team, facilitating smooth execution.",
                ]),
                ("h3", "Problem-Solving and Innovation"),
                ("ul", [
                    "Demonstrate resourcefulness in problem-solving, finding creative solutions to challenges that may arise during project execution.",
                    "Contribute to concept ideation and strategy development.",
                ]),
                ("h3", "Research and Development"),
                ("ul", [
                    "Stay updated on industry trends through research, webinars, and professional development opportunities.",
                    "Assist with industry and market research to support project objectives.",
                    "Analyzing program results and reporting on key insights to help develop action plans.",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "At least 6 months/1year of project / administrative experience within a corporate / agency setting (internship included)",
                    "University degree or equivalent; business, marketing or communications-related preferred",
                    "Previous experience in marketing or communications considered a strong asset",
                    "Prior experience working with social / digital marketing tools (inclusive of social management and listening platforms) considered an asset",
                    "Highly personable and enthusiastic",
                    "Adaptable with an ability to communicate and collaborate with a variety of personality types",
                    "Strong organization and time management skills",
                    "Detail-oriented with a solid work ethic and a genuine eagerness to grow personal skill-set",
                    "Highly developed interpersonal and communication skills, both written and verbal",
                    "Versatile with willingness to learn and work on a diverse collection of projects across varying industries (i.e. technology, finance, education, government, etc.)",
                    "Passionate about modern marketing and tech-innovation",
                    "Ability to work at a fast pace and manage high-stress scenarios",
                    "Self-starter with proven initiative and a solution-based attitude",
                    "Proficient in Microsoft Office and able to work in a digital and cross-functional team environment",
                    "Comfort working with AI-powered tools and modern digital workflows to support day-to-day tasks",
                    "Ability to communicate with confidence and professionalism in senior internal and client-facing environments",
                    "Bilingualism (ENG/FR) considered an asset, but not required",
                ]),
            ]),
        ],
        "why_intercept": None,
        "aiband": [
            "Demonstrate curiosity and openness to new tools, processes, and ways of working",
            "Use AI-powered tools to support tasks such as research, note summarization, and first-draft content development",
            "Apply AI to improve efficiency and organization across day-to-day responsibilities",
            "Build familiarity with how AI is shaping B2B marketing and agency workflows",
            "Bring initiative on how processes could be enhanced with agentic solutions",
        ],
    },

    {
        "slug": "account-manager",
        "title": "Account Manager",
        "tag1": "Client leadership",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "We’re hiring an Account Manager with a minimum 4- to 5-years experience to join Intercept during an exciting evolution of our account model."),
                ("p", "As we introduce a dedicated Integrated Production function owning delivery execution, Account Managers at Intercept are increasingly focused on client leadership, account growth, and commercial continuity."),
                ("p", "This role is ideal for someone who thrives in client-facing environments, builds trust quickly, and is motivated by expanding relationships over time. You will act as the primary owner of assigned client accounts, responsible for nurturing relationships, identifying new opportunities, and driving repeat and expanded engagements, while partnering with Integrated Producers to ensure strong delivery outcomes."),
                ("p", "Account Managers at Intercept are not order-takers. They are strategic partners to clients and active contributors to the agency’s organic growth."),
            ]),
            ("What you’ll do", [
                ("ul", [
                    "Client Leadership & Relationship Management",
                    "Serve as the primary day-to-day client contact and trusted partner across assigned accounts",
                    "Lead client calls with confidence, structure, and clear next steps",
                    "Manage ongoing client communications, ensuring clarity, responsiveness, and professionalism",
                    "Build deep knowledge of client priorities, stakeholders, and internal dynamics",
                    "Maintain strong relationships through proactive engagement, not reactive support",
                    "Account Growth & Expansion (Core Accountability)",
                    "Own post-project follow-on conversations and proactively advance next engagements",
                    "Identify upsell, cross-sell, and expansion opportunities across existing accounts",
                    "Actively “hunt” for new stakeholder relationships, teams, or business units within client organizations",
                    "Partner with Account Directors and Client Pod Leads on account planning, expansion strategy, and pipeline development",
                    "Contribute to shared growth accountability, including pipeline contribution and account expansion goals over time",
                    "Spot client signals early and translate them into concrete opportunities for Intercept",
                    "Delivery Oversight & Project Management",
                    "Provide client-facing oversight across programs while sharing project management responsibilities with Integrated Producers on a project by project basis",
                    "Maintain awareness of timelines, scope, and dependencies to ensure client expectations are met",
                    "Act as an escalation point when risks, changes, or issues arise",
                    "Partner closely with Integrated Producers to ensure alignment between client intent and delivery reality",
                    "Reinforce clarity, prioritization, and accountability across internal and external stakeholders",
                    "Strategic Program & Campaign Oversight",
                    "Contribute to campaign and program strategy alongside Strategy, Content, and Creative teams",
                    "Apply insight from performance data, research, and client feedback to inform recommendations",
                    "Stay conversant in modern B2B marketing, buyer journeys, and AI-enabled approaches to execution",
                    "Documentation, Quality & Communication",
                    "Support creation and maintenance of key client-facing and internal documents (briefs, feedback summaries, recap notes)",
                    "Review deliverables at key milestones to ensure alignment with client expectations and quality standards",
                    "Facilitate internal alignment calls when needed, ensuring clear documentation and follow-through",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "4 to 5+ years of experience in a client-facing role within a marketing agency or client-side environment",
                    "Experience managing and growing client relationships, not just servicing them",
                    "Exposure to B2B marketing, enterprise technology, or complex buyer environments is a strong asset",
                    "Comfortable initiating commercial conversations and advancing opportunities",
                    "Strong written and verbal communication skills with senior client stakeholders",
                    "Highly organized, adaptable, and effective in fast-paced, multi-account environments",
                    "Confident collaborator able to work across strategy, creative, content, and delivery teams",
                    "Strong critical thinking and problem-solving skills",
                    "Demonstrated comfort with AI-powered tools and modern digital workflows",
                    "Proficient in Microsoft Office and collaborative, remote-first work environments",
                    "University degree in Marketing, Business, Communications, or equivalent experience preferred",
                    "Bilingualism (English/French) is an asset but not required",
                ]),
            ]),
        ],
        "why_intercept": [
            "Work with an award-winning B2B marketing agency at the forefront of AI innovation.",
            "Competitive salary, benefits, and professional development opportunities.",
            "You connect with Intercept’s RISE values: Risk, Initiative, Support and Effort.",
            "Use of our company cottage at Innisfil’s Friday Harbour Resort. We’ll even give you a paid day off to enjoy it for a long weekend!",
            "Monthly telecommunications allowance towards use of your home internet and mobile phone.",
            "Comprehensive dental and medical benefits plus a Health Care Spending Account.",
            "Annual wellness fund.",
            "Group RRSP fund-matching program eligible after 3 years in role.",
        ],
        "aiband": [
            "Demonstrate curiosity and openness to new tools, processes, and ways of working",
            "Apply AI-powered tools and workflows to support account planning, insight gathering, and efficiency",
            "Stay informed on industry trends, emerging platforms, and evolving B2B best practices",
            "Bring forward ideas that help Intercept and its clients work smarter, not just harder",
        ],
    },

    {
        "slug": "director-content",
        "title": "Director, Content",
        "tag1": "Content",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "We are looking for a Director, Content with 10+ years of experience in B2B content, editorial, or content marketing. Ideal candidates are experienced content leaders who can define content direction, guide teams, and ensure high-quality, insight-driven content across campaigns and programs."),
                ("p", "They will lead the development and execution of content across formats, including written, video, and audio, ensuring narratives are clear, differentiated, and aligned with audience needs and business objectives. This role requires strong editorial judgment, content strategy experience, and the ability to translate complex inputs into structured, effective content approaches."),
                ("p", "The Director, Content plays a critical role in shaping how content is created, delivered, and scaled across the agency. They lead and mentor writers and editors, contribute to client engagements, and ensure consistency, quality, and performance across all outputs. Candidates should demonstrate strong applied understanding of AI-enabled content workflows that support scalability, efficiency, and continuous improvement."),
            ]),
            ("What you’ll do", [
                ("h3", "Content Direction and Content Strategy"),
                ("ul", [
                    "Develop and execute content strategies aligned with B2B marketing goals and buyer journey stages",
                    "Ensure all content aligns with client objectives, audience needs, and business outcomes",
                    "Translate unclear or unstructured client inputs into clear, actionable content approaches",
                    "Define content frameworks, messaging structures, and narrative direction across programs",
                ]),
                ("h3", "Client Leadership and Engagement"),
                ("ul", [
                    "Lead client workshops and working sessions to clarify messaging and content direction",
                    "Engage directly with clients to refine narratives and align content with business goals",
                    "Present content direction and recommendations clearly and confidently to stakeholders",
                    "Act as a trusted advisor, guiding clients from ambiguity to structured content plans",
                ]),
                ("h3", "Team Leadership and Development"),
                ("ul", [
                    "Lead and mentor a team of writers and editors, setting clear standards for quality and strategic thinking",
                    "Provide coaching, feedback, and direction to elevate team output and performance",
                    "Ensure consistency in voice, messaging, and quality across all deliverables",
                ]),
                ("h3", "Cross-Functional Collaboration"),
                ("ul", [
                    "Collaborate with creative, strategy, and account teams to ensure content integrates effectively into campaigns",
                    "Align content development with broader campaign goals and delivery frameworks",
                ]),
                ("h3", "Content Systems and Operational Excellence"),
                ("ul", [
                    "Bring structure to complex or fast-moving projects, ensuring content development remains clear and aligned",
                    "Establish repeatable frameworks and processes that support scalable content production",
                    "Ensure content output maintains consistency, clarity, and quality across formats and channels",
                ]),
                ("h3", "Thought Leadership and Innovation"),
                ("ul", [
                    "Stay ahead of trends in B2B marketing, content formats, and audience behavior",
                    "Bring forward new ideas, formats, and approaches that strengthen the agency’s content offering",
                    "Contribute to internal thought leadership and the evolution of content practices",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "10+ years of experience in B2B content, editorial, or content marketing",
                    "Strong background in writing and editorial work, with experience leading content development",
                    "Deep understanding of B2B marketing, particularly within the technology sector",
                    "Experience working with enterprise clients and leading complex content engagements",
                    "Familiarity with written, video, and audio content formats",
                    "Strong communication skills with the ability to lead client discussions and workshops",
                    "Experience managing multiple projects and maintaining high-quality output under pressure",
                    "Demonstrated ability to apply and lead adoption of AI-powered tools to enhance content development, quality, and scalability",
                ]),
            ]),
        ],
        "why_intercept": [
            "Work with an award-winning B2B marketing agency at the forefront of AI innovation.",
            "Competitive salary, benefits, and professional development opportunities.",
            "You connect with Intercept’s RISE values: Risk, Initiative, Support and Effort.",
            "Use of our company cottage at Innisfil’s Friday Harbour Resort. We’ll even give you a paid day off to enjoy it for a long weekend!",
            "Monthly telecommunications allowance towards use of your home internet and mobile phone.",
            "Comprehensive dental and medical benefits plus a Health Care Spending Account.",
            "Annual wellness fund.",
            "Group RRSP fund-matching program eligible after 3 years in role.",
        ],
        "aiband": [
            "Lead adoption of AI-enabled tools and workflows across the content team",
            "Apply AI to support content development, research, and scaling across formats and channels",
            "Identify opportunities to integrate AI into content systems, personalization, and production workflows",
            "Guide the team in using AI effectively while maintaining strong editorial standards and brand voice",
            "Stay informed on emerging AI capabilities and translate them into practical applications for clients and internal teams",
        ],
    },

    {
        "slug": "graphic-designer-ui-ux",
        "title": "Graphic Designer, UI-UX",
        "tag1": "Creative",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "We are looking for skilled Graphic Designers with 3 to 5 years of experience in a marketing agency or similar environment. Ideal candidates are strong visual thinkers with a passion for modern design, capable of executing high-quality creative across a range of B2B marketing assets."),
                ("p", "They will support the development and execution of creative deliverables across campaigns, working closely with creative leads, account teams, and other specialists to bring ideas to life. This role requires strong attention to detail, adaptability, and the ability to manage multiple projects in a fast-paced environment."),
                ("p", "Candidates should demonstrate curiosity and openness to modern design tools and AI-enabled workflows that support creative exploration, production efficiency, and asset development."),
            ]),
            ("What you’ll do", [
                ("h3", "Meeting Participation and Communication"),
                ("ul", [
                    "Take comprehensive notes during internal and client calls, ensuring important details are captured and acted upon.",
                    "Proactively identify opportunities for improvement and contribute innovative ideas during briefing calls and all-hands meetings.",
                    "Actively participate in internal brief calls, providing input and insights to shape project direction and objectives.",
                    "Respond promptly to internal briefs and maintain clear communication with account teams throughout the project lifecycle.",
                    "Prepare and deliver materials for internal studio all-hands meetings to foster team collaboration and alignment.",
                    "Participate in internal studio team sync meetings, identifying challenges and proposing solutions to drive project success.",
                ]),
                ("h3", "Project Management"),
                ("ul", [
                    "Manage workback schedules for project deliverables, ensuring deadlines are met and team members are informed of their responsibilities.",
                    "Effectively manage time and prioritize tasks to meet project deadlines and handle multiple projects simultaneously.",
                    "Navigate context switching and client feedback rounds with ease, demonstrating urgency and balancing workload effectively.",
                    "Manage bandwidth effectively and communicate project timelines with team members to optimize project workflow.",
                    "Clearly understand project requirements and communicate effectively with team members to ensure alignment and successful project execution.",
                ]),
                ("h3", "Creative Design and Execution"),
                ("ul", [
                    "Develop and maintain interactive pages, tools, and digital experiences using Coda or similar platforms.",
                    "Translate strategic, creative, or technical requirements into functional interactive experiences.",
                    "Build clean, user-friendly layouts that organize information clearly and support strong navigation.",
                    "Create interactive components such as buttons, filters, calculators, forms, dashboards, quizzes, assessments, tables, databases, conditional logic, and dynamic content views.",
                    "Collaborate with strategy, creative, content, and client teams to understand objectives and recommend the best format for the experience.",
                    "Ensure digital experiences are easy to use, visually polished, logically structured, and aligned with brand guidelines.",
                    "Test interactive experiences for usability, accuracy, broken links, permissions, mobile responsiveness, and overall quality.",
                    "Document how experiences are built so internal teams or clients can update them confidently.",
                    "Identify opportunities to improve workflows, automate repetitive tasks, or make content more engaging through interactivity.",
                    "Develop wireframes and design user interfaces for websites, ensuring a seamless and intuitive user experience.",
                    "Create wireframes and design email templates for various marketing campaigns and communications.",
                    "Demonstrate creative prowess by generating original ideas and designs that align with brand guidelines and client briefs.",
                    "Maintain accuracy in creative composition and execution, ensuring designs meet client expectations and project requirements.",
                    "Required to learn and use different design platforms and formats as directed by leadership.",
                    "Conduct self-reviews of creative assets to ensure they meet quality standards and adhere to the asset review submission process.",
                ]),
                ("h3", "Problem-Solving and Innovation"),
                ("ul", [
                    "Demonstrate resourcefulness in problem-solving, finding creative solutions to challenges as they arise during the design process.",
                ]),
                ("h3", "Research and Development"),
                ("ul", [
                    "Stay updated on industry trends through research, webinars, and professional development opportunities to enhance design skills and stay ahead of the curve.",
                    "Thoroughly understand client briefs and project requirements to inform design decisions and deliver exceptional results.",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "At least 3-5 years of graphic design experience with a UI/UX focus background",
                    "Strong understanding of information architecture, user experience, and content organization.",
                    "Ability to build interactive pages, databases, forms, dashboards, and dynamic content systems.",
                    "Comfort working with formulas, conditional logic, filters, views, buttons, and basic automation.",
                    "Experience working in a marketing agency or marketing department considered a strong asset",
                    "Experience building microsites, resource hubs, campaign pages, sales enablement tools, or client-facing interactive experiences.",
                    "Basic understanding of HTML, CSS, JavaScript, APIs, or embedded content.",
                    "Prior exposure to B2B marketing within various industries (including technology, finance, education, etc.), considered a strong asset",
                    "Deep knowledge and experience in Figma and UI/UX design required",
                    "Must design in Figma first to facilitate interactive builds",
                    "Must know Adobe Illustrator and Photoshop",
                    "Experience adhering to corporate brand guidelines",
                    "Experience in photo editing/manipulation, vector art design, and illustration",
                    "Experience in creating digital display banners and wireframing emails and web pages",
                    "Passionate about modern marketing and tech-innovation",
                    "Proficient in Microsoft Office and able to work within in-person and remote team environments",
                    "Highly developed interpersonal and communication skills, both written and verbal",
                    "Strong organizational and time management skills with ability to work at a fast pace",
                    "Self-starter with proven initiative and resourcefulness",
                    "Solution-based with ability to collaborate with colleagues and other partners",
                    "Willingness and capability to work on multiple accounts and handle diverse projects",
                    "Comfort working with AI-powered tools to support creative development, production efficiency, and asset creation",
                    "Bilingualism (ENG/FR) considered an asset, but not required",
                ]),
            ]),
        ],
        "why_intercept": [
            "Use of our company cottage at Innisfil’s Friday Harbour Resort. We’ll even give you a paid day off to enjoy it for a long weekend!",
            "Monthly telecommunications allowance towards use of your home internet and mobile phone.",
            "Comprehensive dental and medical benefits plus a Health Care Spending Account.",
            "Annual wellness fund.",
            "Group RRSP fund-matching program eligible after 3 years in role.",
            "Work with an award-winning B2B marketing agency at the forefront of AI innovation.",
            "Competitive salary, benefits, and professional development opportunities.",
            "You connect with Intercept’s RISE values: Risk, Initiative, Support and Effort.",
        ],
        "aiband": [
            "Demonstrate curiosity and openness to new tools, technologies, and ways of working",
            "Use AI-powered tools to support ideation, layout exploration, and production efficiency",
            "Apply AI to assist with tasks such as image generation, content adaptation, and asset variation",
            "Incorporate AI-enabled workflows to streamline repetitive design tasks and improve output speed",
            "Stay informed on how AI is shaping creative development and bring forward ideas to improve workflows",
        ],
    },

    {
        "slug": "graphic-designer",
        "title": "Graphic Designer",
        "tag1": "Creative",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "We are looking for skilled Graphic Designers with 3 to 5 years of experience in a marketing agency or similar environment. Ideal candidates are strong visual thinkers with a passion for modern design, capable of executing high-quality creative across a range of B2B marketing assets."),
                ("p", "They will support the development and execution of creative deliverables across campaigns, working closely with creative leads, account teams, and other specialists to bring ideas to life. This role requires strong attention to detail, adaptability, and the ability to manage multiple projects in a fast-paced environment."),
                ("p", "Candidates should demonstrate curiosity and openness to modern design tools and AI-enabled workflows that support creative exploration, production efficiency, and asset development."),
            ]),
            ("What you’ll do", [
                ("h3", "Meeting Participation and Communication"),
                ("ul", [
                    "Take comprehensive notes during internal and client calls, ensuring important details are captured and acted upon.",
                    "Proactively identify opportunities for improvement and contribute innovative ideas during briefing calls and all-hands meetings.",
                    "Actively participate in internal brief calls, providing input and insights to shape project direction and objectives.",
                    "Respond promptly to internal briefs and maintain clear communication with account teams throughout the project lifecycle.",
                    "Prepare and deliver materials for internal studio all-hands meetings to foster team collaboration and alignment.",
                    "Participate in internal studio team sync meetings, identifying challenges and proposing solutions to drive project success.",
                ]),
                ("h3", "Project Management"),
                ("ul", [
                    "Manage workback schedules for project deliverables, ensuring deadlines are met and team members are informed of their responsibilities.",
                    "Effectively manage time and prioritize tasks to meet project deadlines and handle multiple projects simultaneously.",
                    "Navigate context switching and client feedback rounds with ease, demonstrating urgency and balancing workload effectively.",
                    "Manage bandwidth effectively and communicate project timelines with team members to optimize project workflow.",
                    "Clearly understand project requirements and communicate effectively with team members to ensure alignment and successful project execution.",
                ]),
                ("h3", "Creative Design and Execution"),
                ("ul", [
                    "Demonstrate creative prowess by generating original ideas and designs that align with brand guidelines and client briefs.",
                    "Maintain accuracy in creative composition and execution, ensuring designs meet client expectations and project requirements.",
                    "Required to learn and use different design platforms and formats as directed by leadership.",
                    "Conduct self-reviews of creative assets to ensure they meet quality standards and adhere to the asset review submission process.",
                    "Develop wireframes and design user interfaces for websites, ensuring a seamless and intuitive user experience.",
                    "Create wireframes and design email templates for various marketing campaigns and communications.",
                    "Develop and edit PowerPoint presentations for both agency and client use, ensuring clear and engaging visual communication.",
                    "Prepare alone or with an animator, static frame-by-frame layout for animated display, social, or other animated format.",
                    "Design layouts for B2B marketing assets such as eBooks, whitepapers, and infographics, ensuring clarity and visual appeal.",
                    "Create static and animated social media posts to engage audiences and support marketing campaigns.",
                    "Design and produce various print media materials including flyers, posters, one-pagers, direct mail, premiums/swag, vinyl wraps, and environmental branding.",
                ]),
                ("h3", "Problem-Solving and Innovation"),
                ("ul", [
                    "Demonstrate resourcefulness in problem-solving, finding creative solutions to challenges as they arise during the design process.",
                ]),
                ("h3", "Research and Development"),
                ("ul", [
                    "Stay updated on industry trends through research, webinars, and professional development opportunities to enhance design skills and stay ahead of the curve.",
                    "Thoroughly understand client briefs and project requirements to inform design decisions and deliver exceptional results.",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "At least 3-5 years of graphic design experience with a UI/UX focus background",
                    "Experience working in a marketing agency or marketing department considered a strong asset",
                    "Prior exposure to B2B marketing within various industries (including technology, finance, education, etc.), considered a strong asset",
                    "Deep knowledge and experience in Figma and UI/UX design required",
                    "Must know Adobe Illustrator and Photoshop",
                    "Experience adhering to corporate brand guidelines",
                    "Experience in PowerPoint presentation design",
                    "Experience in photo editing/manipulation, vector art design, and illustration",
                    "Experience in creating digital display banners and wireframing emails and web pages",
                    "Experience in 3D modelling/rendering (i.e. Maya, Houdini, Cinema 4D, 3DS Max, Blender, etc.) considered an asset, though not required",
                    "Passionate about modern marketing and tech-innovation",
                    "Proficient in Microsoft Office and able to work within in-person and remote team environments",
                    "Highly developed interpersonal and communication skills, both written and verbal",
                    "Strong organizational and time management skills with ability to work at a fast pace",
                    "Self-starter with proven initiative and resourcefulness",
                    "Solution-based with ability to collaborate with colleagues and other partners",
                    "Willingness and capability to work on multiple accounts and handle diverse projects",
                    "Comfort working with AI-powered tools to support creative development, production efficiency, and asset creation",
                    "Bilingualism (ENG/FR) considered an asset, but not required",
                ]),
            ]),
        ],
        "why_intercept": [
            "Use of our company cottage at Innisfil’s Friday Harbour Resort. We’ll even give you a paid day off to enjoy it for a long weekend!",
            "Monthly telecommunications allowance towards use of your home internet and mobile phone.",
            "Comprehensive dental and medical benefits plus a Health Care Spending Account.",
            "Annual wellness fund.",
            "Group RRSP fund-matching program eligible after 3 years in role.",
            "Work with an award-winning B2B marketing agency at the forefront of AI innovation.",
            "Competitive salary, benefits, and professional development opportunities.",
            "You connect with Intercept’s RISE values: Risk, Initiative, Support and Effort.",
        ],
        "aiband": [
            "Demonstrate curiosity and openness to new tools, technologies, and ways of working",
            "Use AI-powered tools to support ideation, layout exploration, and production efficiency",
            "Apply AI to assist with tasks such as image generation, content adaptation, and asset variation",
            "Incorporate AI-enabled workflows to streamline repetitive design tasks and improve output speed",
            "Stay informed on how AI is shaping creative development and bring forward ideas to improve workflows",
        ],
    },

    {
        "slug": "integrated-producer",
        "title": "Integrated Producer",
        "tag1": "Operations",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "We’re looking for an Integrated Producer to lead the planning, execution, and delivery of mid- to large-scale integrated campaigns with many different asset types, managing workflows across creative, strategy, content, and production partners. This role oversees projects from scoping through post-production, proactively driving timelines, budgets, communication, and quality. The Integrated Producer is a confident operator who owns day-to-day production, ensures every deliverable is polished, on time and on brand."),
            ]),
            ("What you’ll do", [
                ("ul", [
                    "Project Ownership",
                    "Lead end-to-end project planning, scoping, timelines, and resourcing across assigned initiatives, leveraging waterfall/agile/sprint methodologies as needed to streamline delivery.",
                    "Own project setup and infrastructure (PM tools, file organization, workflow structure), along with key documentation and requirements (SOWs, change orders, technical specs, delivery guidelines).",
                    "Drive production across digital, social, video, experiential, and multi-channel deliverables from kickoff through final delivery.",
                    "Serve as the primary production lead, partnering with account, strategy, and creative teams to align on scope, expectations, feasibility, and actionable production plans.",
                    "Maintain schedules, status reporting, and internal reviews/approval cycles, distributing meeting notes and action items to keep teams aligned and projects moving forward.",
                    "Cross-Functional Collaboration",
                    "Partner with creative, content, strategy, production, and account lead to clarify briefs, refine specs, confirm scope, and ensure deliverables align with brand, technical requirements, and feasibility.",
                    "Communicate proactively with internal teams, vendors, and freelancers to set expectations, resolve blockers, and maintain alignment throughout the project lifecycle.",
                    "Oversee asset delivery processes on your projects, ensuring files are organized, version-controlled, correctly formatted/named, and delivered accurately across platforms.",
                    "Own resourcing for assigned projects, assessing availability and skill fit, forecasting needs across phases, and onboarding freelancers/vendors as needed.",
                    "Quality, Process, & Problem Solving",
                    "Maintain production quality across all workstreams, ensuring deliverables meet brand, creative, technical, and platform standards.",
                    "Manage internal reviews, feedback cycles, revisions, and approvals to ensure smooth progress and alignment.",
                    "Perform light QC including proofreading, formatting checks, accessibility reviews, and final asset prep for delivery.",
                    "Anticipate risks early, proactively mitigate issues, and resolve blockers to keep projects on track.",
                    "Contribute to optimizing project workflows and production practices, communication, and exploring new tools, automation, and AI enhancements while upholding PMO standards",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "5 to 8 years of project management or integrated production experience in at a marketing/advertising agency that includes experience in managing a variety of campaign and creative digital assets (banners, eBooks/guides, social, webinars, landing pages, case studies, emails etc.) with multiple versions/outputs",
                    "Proven ability to manage tight timelines, vendors, and complex multi-channel workflows.",
                    "Strong technical understanding of digital specs, AI, video deliverables, file formats, and platform requirements.",
                    "Experience leading production conversations and presenting production plans.",
                    "Highly organized, deadline-driven, and able to manage multiple workstreams concurrently.",
                    "Familiarity with PM tools (Asana, Monday.com, Smartsheet, Jira) and digital delivery systems.",
                    "Skilled in Quality Control, reviewing/proofreading with attention to detail and light editing when needed",
                    "Strong project management skills including scheduling, budgeting, and resource planning.",
                    "Exceptional attention to detail and commitment to quality.",
                    "Calm, steady, and collaborative team player with strong communication skills across all internal audiences (executives, directors, and project teams), able to read the room and tailor messaging and level of detail as needed.",
                    "A solution-oriented clear communicator and natural collaborator in a remote-first team.",
                    "A positive attitude with curiosity for new technologies and production innovations.",
                    "Proficiency in Microsoft Suite",
                ]),
            ]),
        ],
        "why_intercept": [
            "Comprehensive benefits package",
            "Fully remote work with flexible hours and core collaboration times",
            "The opportunity to lead high-impact campaigns for enterprise technology brands",
            "Professional growth across integrated production, project management practices across a wide range of material",
            "A collaborative, creative, award-winning team culture",
        ],
        "aiband": [
            "Demonstrate curiosity and openness to new tools, processes, and ways of working",
            "Apply AI-powered tools to support project planning, scheduling, and workflow optimization",
            "Use AI to assist with asset tracking, version control, documentation, and production efficiency",
            "Explore automation and AI-enabled solutions to streamline production processes and improve delivery speed",
            "Stay informed on emerging production tools and bring forward ideas that enhance team efficiency and output quality",
        ],
    },

    {
        "slug": "senior-account-manager",
        "title": "Sr. Account Manager",
        "tag1": "Client leadership",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "We are looking for skilled Senior Account Managers with 4 to 5+ years of experience in client-facing roles within an agency or fast-paced environment. Ideal candidates are strong relationship builders and strategic thinkers, capable of leading client engagements while managing multiple programs across complex B2B marketing initiatives."),
                ("p", "They will own day-to-day client relationships, oversee program delivery, and contribute to account growth by identifying opportunities and maintaining strong momentum across engagements. This role also includes leadership of internal pods, ensuring alignment, accountability, and high-quality execution across teams."),
                ("p", "Candidates should demonstrate curiosity and applied understanding of modern marketing tools and AI-enabled workflows that support efficient delivery, stronger insights, and smarter ways of working."),
            ]),
            ("What you’ll do", [
                ("h3", "Client Interaction and Support"),
                ("ul", [
                    "Manage the flow of client calls, ensuring all key points are covered.",
                    "Take detailed notes to capture important discussions, action items, and decisions.",
                    "Develop and nurture strong relationships with clients by understanding their needs and demonstrating confidence in our services.",
                    "Identify and generate new business opportunities through awareness and proactive outreach.",
                    "Conduct cold outreach to potential clients to expand our business.",
                    "Provide timely and professional email support to clients, managing day-to-day communications and weekly deliverables.",
                ]),
                ("h3", "Project Documentation and Quality Assurance"),
                ("ul", [
                    "Create and maintain project documents, including internal briefs, client feedback, and communication within the studio team.",
                    "Perform quality assurance checks on project assets to ensure they meet the highest standards of quality and accuracy.",
                ]),
                ("h3", "Internal Communication and Collaboration"),
                ("ul", [
                    "Facilitate internal calls such as briefing and all-hands meetings.",
                    "Take detailed notes to capture key discussions and action items.",
                    "Prepare materials for and contribute to the delivery of internal account all-hands meetings to foster team alignment and strategy execution.",
                ]),
                ("h3", "People Management"),
                ("ul", [
                    "Oversee and manage team members, providing leadership, direction, and support.",
                    "Conduct or contribute to regular performance reviews and provide constructive feedback to team members.",
                    "Foster a positive and collaborative team environment, encouraging professional growth and development.",
                    "Address and resolve any team conflicts or issues promptly and effectively.",
                ]),
                ("h3", "Project Management leadership"),
                ("ul", [
                    "Use project management tools to manage project tasks, assign responsibilities, and monitor progress.",
                    "Work in close collaboration with with an Integrated Producer who lead project management of their project, while the Sr Account Manager leads the client relationship and communication",
                    "Lead and manage project pods, building relationships and providing support, guidance, mentoring, coaching, and feedback to team members.",
                    "Manage team bandwidth and communicate project timelines to ensure efficient project delivery.",
                    "Clearly understand project requirements and effectively communicate them to the team.",
                ]),
                ("h3", "Problem-Solving and Innovation"),
                ("ul", [
                    "Demonstrate resourcefulness in solving problems and finding creative solutions to challenges.",
                ]),
                ("h3", "Research and Development"),
                ("ul", [
                    "Stay updated on industry trends through research, webinars, and professional development opportunities.",
                ]),
                ("h3", "Project Planning and Execution"),
                ("ul", [
                    "Thoroughly understand client briefs to facilitate effective project planning and execution",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "4 to 5+ years of experience in a client-facing role within a marketing agency or client-side environment",
                    "Experience managing and growing client relationships, not just servicing them",
                    "Exposure to B2B marketing, enterprise technology, or complex buyer environments is a strong asset",
                    "Comfortable initiating commercial conversations and advancing opportunities",
                    "Strong written and verbal communication skills with senior client stakeholders",
                    "Highly organized, adaptable, and effective in fast-paced, multi-account environments",
                    "Confident collaborator able to work across strategy, creative, content, and delivery teams",
                    "Strong critical thinking and problem-solving skills",
                    "Demonstrated experience applying AI-powered tools and workflows to improve efficiency, insight generation, and execution",
                    "Proficient in Microsoft Office and collaborative, remote-first work environments",
                    "University degree in Marketing, Business, Communications, or equivalent experience preferred",
                    "Bilingualism (English/French) is an asset but not required",
                ]),
            ]),
        ],
        "why_intercept": [
            "Work with an award-winning B2B marketing agency at the forefront of AI innovation.",
            "Competitive salary, benefits, and professional development opportunities.",
            "You connect with Intercept’s RISE values: Risk, Initiative, Support and Effort.",
            "Use of our company cottage at Innisfil’s Friday Harbour Resort. We’ll even give you a paid day off to enjoy it for a long weekend!",
            "Monthly telecommunications allowance towards use of your home internet and mobile phone.",
            "Comprehensive dental and medical benefits plus a Health Care Spending Account.",
            "Annual wellness fund.",
            "Group RRSP fund-matching program eligible after 3 years in role.",
        ],
        "aiband": [
            "Demonstrate curiosity and openness to new tools, processes, and ways of working",
            "Apply AI-powered tools and workflows to support account planning, insight generation, and team efficiency",
            "Use AI to enhance research, communication, and documentation across client programs",
            "Identify opportunities to improve workflows and ways of working through AI-enabled approaches",
            "Stay informed on how AI is shaping B2B marketing and bring forward ideas that improve team and client outcomes",
        ],
    },

    {
        "slug": "senior-copywriter",
        "title": "Sr. Copywriter",
        "tag1": "Content",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "The Sr. Copywriter is responsible for developing high-quality, in-depth content that informs, engages, and builds trust with target audiences. This role focuses on crafting compelling narratives across formats such eBooks, whitepapers, reports, guides, infographics, case studies, blogs and other medium to long-form editorial content that support brand positioning and long-term audience engagement."),
                ("p", "Working at the intersection of storytelling and strategy, the Sr. Copywriter translates complex ideas into clear, structured, and engaging content aligned with brand voice and business objectives. This role collaborates cross-functionally to deliver content that drives awareness, strengthens credibility, and supports the full customer journey."),
            ]),
            ("What you’ll do", [
                ("h3", "Content Development"),
                ("ul", [
                    "Create compelling, in-depth written content including, but not limited to, eBooks, whitepapers, reports, guides, infographics, case studies, and blogs.",
                    "Write clear, engaging, and well-researched medium and long-form copy that educates, informs, and builds trust with target audiences.",
                    "Translate complex ideas into accessible, structured narratives that align with brand voice and business objectives.",
                    "Balance storytelling with strategic intent, ensuring content drives awareness, consideration, and long-term engagement.",
                ]),
                ("h3", "Content Strategy and Editorial Planning"),
                ("ul", [
                    "Develop and execute long-form content strategies aligned with marketing goals, audience needs, and SEO/GEO/AEO best practices.",
                    "Generate content ideas using data, customer insights, and industry trends to support thought leadership and organic growth.",
                    "Plan and manage editorial calendars to ensure consistency and relevance across all long-form content initiatives.",
                    "Maintain a cohesive brand voice across extended narratives while adapting tone and depth depending on the audience and channel.",
                ]),
                ("h3", "Research and Insight Development"),
                ("ul", [
                    "Conduct thorough research to support content accuracy, credibility, and authority.",
                    "Synthesize information from multiple sources, including internal stakeholders, subject matter experts, and external research.",
                    "Identify key themes and insights that position the brand as a leader within its industry.",
                ]),
                ("h3", "Collaboration and Communication"),
                ("ul", [
                    "Work cross-functionally with marketing, product, design, and subject matter experts to develop high-quality content.",
                    "Collaborate with content marketing, product marketing, and brand teams to ensure content is optimized and aligned with broader campaigns.",
                    "Present ideas and content concepts clearly, incorporating feedback from stakeholders at all levels.",
                ]),
                ("h3", "Quality Assurance and Editorial Excellence"),
                ("ul", [
                    "Ensure all content is polished, accurate, and aligned with brand guidelines and editorial standards.",
                    "Edit and proofread medium and long-form content with strong attention to structure, tone, clarity, and flow.",
                    "Maintain consistency in messaging while elevating the overall quality and sophistication of written materials.",
                ]),
                ("h3", "Performance Optimization and Continuous Improvement"),
                ("ul", [
                    "Use AI tools to draft outlines and V1s, incorporate client feedback, pressure-test clarity and flow, and validate claims.",
                    "Analyze content performance metrics (e.g., engagement, time on page, conversions) to refine future content.",
                    "Iterate on content based on data insights, audience behavior, and evolving business priorities.",
                    "Continuously explore new formats, storytelling techniques, and content opportunities to improve effectiveness.",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "Proficient in the use of AI tools to assist copywriting processes (GPT, Grammerly, etc.)",
                    "Proficient in Microsoft Office and able to work in a digital and cross-functional team environment",
                    "Bilingualism (ENG/FR) considered an asset, but not required",
                ]),
            ]),
        ],
        "why_intercept": [
            "Use of our company cottage at Innisfil’s Friday Harbour Resort. We’ll even give you a paid day off to enjoy it for a long weekend!",
            "Monthly telecommunications allowance towards use of your home internet and mobile phone.",
            "Comprehensive dental and medical benefits plus a Health Care Spending Account.",
            "Annual wellness fund.",
            "Group RRSP fund-matching program. Eligible after 3 years in role.",
            "Work with an award-winning B2B marketing agency at the forefront of AI innovation.",
            "Competitive salary, benefits, and professional development opportunities.",
            "You connect with Intercept’s RISE values: Risk, Initiative, Support and Effort.",
        ],
        "aiband": [
            "Apply AI-powered tools to support medium and long-form content development, editing, and iteration",
            "Use AI to improve efficiency in research, structuring, and content repurposing",
            "Experiment with AI to enhance storytelling, clarity, and content performance",
            "Stay informed on how AI is shaping content creation and bring forward ideas to improve workflows",
        ],
    },

    {
        "slug": "senior-editorial-manager",
        "title": "Senior Editorial Manager",
        "tag1": "Content",
        "tag2": "Full-time · Remote",
        "sections": [
            ("The role", [
                ("p", "We are looking for a Senior Editorial Manager with 10+ years of experience in editorial, copy editing, or content strategy within a B2B or agency environment. Ideal candidates are experienced editors and content leaders who can refine messaging, elevate storytelling, and ensure consistency and quality across all written content."),
                ("p", "They will oversee editorial quality across campaigns and content, working closely with writers, designers, and account teams to ensure copy is clear, compelling, and aligned with brand voice and strategic objectives. This role requires strong editorial judgment, attention to detail, and the ability to guide both content and teams toward stronger outcomes."),
                ("p", "Senior Editorial Managers at Intercept are both craft leaders and collaborators. They mentor writers, contribute to client conversations, and help shape how content is developed and delivered across the agency. Candidates should demonstrate strong applied understanding of AI-enabled editorial workflows that support content refinement, consistency, and efficiency."),
            ]),
            ("What you’ll do", [
                ("h3", "Editorial Leadership and Quality"),
                ("ul", [
                    "Refine and elevate copy across multiple formats, including emails, eBooks, video scripts, and digital campaigns",
                    "Ensure consistency in messaging, tone, and voice across brands, projects, and platforms",
                    "Apply strong editorial judgment to improve clarity, structure, storytelling, and overall impact",
                ]),
                ("h3", "Client Leadership and Communication"),
                ("ul", [
                    "Present copy and narrative direction to clients, leading discussions and working sessions to refine messaging",
                    "Work with the account team to facilitate client exchanges, ensuring a smooth process from initial drafts to final approvals",
                ]),
                ("h3", "Team Leadership and Development"),
                ("ul", [
                    "Mentor and develop writers, providing guidance to help them produce stronger, more strategic content",
                    "Support the growth and development of editorial standards across the team",
                ]),
                ("h3", "Collaboration and Integration"),
                ("ul", [
                    "Collaborate with the creative team, including designers, to refine copy in layouts and ensure messaging is visually and contextually compelling",
                    "Work cross-functionally with account, strategy, and content teams to deliver integrated campaigns",
                ]),
                ("h3", "Editorial Strategy and Standards"),
                ("ul", [
                    "Support special agency projects, such as developing the Intercept brand voice and editorial guidelines",
                    "Contribute to maintaining and evolving editorial frameworks, standards, and best practices",
                ]),
                ("h3", "Research and Development"),
                ("ul", [
                    "Stay informed on industry trends, content practices, and evolving editorial approaches",
                ]),
            ]),
            ("What you bring", [
                ("ul", [
                    "10+ years of experience in editorial, copy editing, content strategy, or a similar role",
                    "Experience working with enterprise brands in the B2B technology sector",
                    "Strong editorial judgment with the ability to refine and elevate content",
                    "Experience leading client discussions and facilitating working sessions to refine messaging",
                    "Experience mentoring and developing writing talent",
                    "Ability to collaborate with designers and creative teams to refine copy in layouts",
                    "Fluency with AI tools such as ChatGPT, Grammerly and other writing assistants to support editorial workflows",
                    "Strong communication and collaboration skills",
                    "Why Join Our Team?",
                ]),
            ]),
        ],
        "why_intercept": [
            "Use of our company cottage at Innisfil’s Friday Harbour Resort. We’ll even give you a paid day off to enjoy it for a long weekend.",
            "Monthly telecommunications allowance towards use of your home internet and mobile phone.",
            "Health and dental benefits plus a Health Care Spending Account.",
            "Annual wellness fund.",
            "Group RRSP fund-matching program eligible after three years in role.",
        ],
        "aiband": [
            "Proficiency in AI tools such as ChatGPT, Grammerly and similar platforms to enhance editorial workflows",
            "Apply AI to support editing, versioning, and consistency across content at scale",
            "Identify opportunities to integrate AI into editorial processes to improve efficiency and quality",
            "Guide writers in using AI effectively while maintaining strong editorial standards and brand voice",
        ],
    },

]


def render(role):
    title = role["title"]
    base = "../../../"
    apply_href = "../../apply/index.html"

    main_sections_html = "".join(sec(t, b) for t, b in role["sections"])

    aiband_html = f"""<section class="aiband">
  <div class="wrap">
    <h2>How we work with AI</h2>
    <p class="lede">{esc(AI_INTRO)}</p>
    {ul_html(role["aiband"])}
  </div>
</section>"""

    why_html = ""
    if role.get("why_intercept"):
        why_html = f"""<div class="rbody">
  <div class="wrap">
    {sec("Why Intercept", [("ul", role["why_intercept"])])}
  </div>
</div>"""

    return f"""<!doctype html>
<html lang="en">
<head>
{head_html(f"{title} · Intercept", f"{title} — an open role at Intercept.")}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(base)}
<main id="main">

<div class="crumb"><div class="crumb-row">Careers · Open roles · <b>{esc(title)}</b></div></div>

<section class="rhero">
  <div class="wrap">
    <span class="eyebrow">Open role</span>
    <h1>{esc(title)}</h1>
    <div class="rmeta">
      <span class="rtag">{esc(role["tag1"])}</span>
      <span class="rtag">{esc(role["tag2"])}</span>
    </div>
    <a class="btn" href="{apply_href}">Apply for this role</a>
  </div>
</section>

<div class="rbody">
  <div class="wrap">
    {main_sections_html}
  </div>
</div>

{aiband_html}

{why_html}

<section class="apply">
  <div class="wrap read">
    <h2>{esc(APPLY_H2)}</h2>
    <p>{esc(APPLY_P)}</p>
    <a class="btn" href="{apply_href}">Apply for this role</a>
  </div>
</section>

</main>
{footer_html(base)}
</body>
</html>"""


if __name__ == "__main__":
    for role in ROLES:
        outdir = os.path.join(ROOT, "careers", "open-roles", role["slug"])
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "index.html")
        open(path, "w", encoding="utf-8").write(render(role))
        print("Wrote", path)
