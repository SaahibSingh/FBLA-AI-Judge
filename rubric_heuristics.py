#Imports
from __future__ import annotations
import math
from typing import Optional

# 1.  RUBRIC CATALOGUE
#     Each event entry lists the rubric criteria with their official point
#     ranges, drawn directly from the 2025-2026 FBLA rating sheets.

# Shared delivery criteria appear on virtually every rating sheet.
_DELIVERY_CRITERIA = {
    "delivery_organization": {
        "label": "Statements well-organized and clearly stated",
        "max_points": 10,
        "feature_group": "delivery_org",
    },
    "delivery_confidence": {
        "label": "Confidence, body language, eye contact, voice projection",
        "max_points": 10,
        "feature_group": "delivery_conf",
    },
    "delivery_qa": {
        "label": "Ability to effectively answer questions",
        "max_points": 10,
        "feature_group": "delivery_qa",
    },
}

# Protocol adherence (binary: 0 or max_points).
_PROTOCOL_CRITERION = {
    "protocol": {
        "label": "Adherence to Competitive Events Guidelines",
        "max_points": 10,
        "feature_group": "protocol",
    }
}

EVENTS: dict[str, dict] = {
    # ── Introduction to Business Presentation ────────────────────────────────
    "IntroductiontoBusinessPresentation": {
        "total_points": 115,
        "criteria": {
            "topic_understanding": {
                "label": "Demonstrates understanding of event topic (industry terminology)",
                "max_points": 15,
                "feature_group": "content_topic",
            },
            "purpose_logical_flow": {
                "label": "Describes purpose with a logical sequence of ideas",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "summary_recommendations": {
                "label": "Summarizes information and identifies recommendations",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "technology_design": {
                "label": "Technology/design: proper formatting and business presentation features",
                "max_points": 15,
                "feature_group": "slide_design",
            },
            "accuracy_sources": {
                "label": "Uses suitable and accurate statements; cites sources",
                "max_points": 15,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Introduction to Public Speaking ──────────────────────────────────────
    "IntroductiontoPublicSpeaking": {
        "total_points": 110,
        "criteria": {
            "topic_theme": {
                "label": "Incorporates provided topic; consistent theme",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "introduction": {
                "label": "Introduce the speech clearly",
                "max_points": 10,
                "feature_group": "structure_intro",
            },
            "body": {
                "label": "Supporting information, body of speech",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "conclusion": {
                "label": "Effective conclusion connected to topic/theme",
                "max_points": 10,
                "feature_group": "structure_conclusion",
            },
            "delivery_pace_filler": {
                "label": "Appropriate pace, lack of filler words",
                "max_points": 10,
                "feature_group": "delivery_pace",
            },
            "delivery_eye_facial": {
                "label": "Eye contact, varied facial expressions",
                "max_points": 10,
                "feature_group": "delivery_conf",
            },
            "delivery_voice": {
                "label": "Voice projection",
                "max_points": 10,
                "feature_group": "delivery_voice",
            },
            "delivery_confidence_posture": {
                "label": "Self-confidence, poise, posture",
                "max_points": 10,
                "feature_group": "delivery_conf",
            },
            "delivery_qa": {
                "label": "Ability to effectively answer questions",
                "max_points": 10,
                "feature_group": "delivery_qa",
            },
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Public Speaking ───────────────────────────────────────────────────────
    "PublicSpeaking": {
        "total_points": 110,
        "criteria": {
            "topic_theme": {
                "label": "Incorporates provided topic; consistent theme",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "introduction": {
                "label": "Introduce the speech",
                "max_points": 10,
                "feature_group": "structure_intro",
            },
            "body": {
                "label": "Supporting information, body",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "conclusion": {
                "label": "Effective conclusion",
                "max_points": 10,
                "feature_group": "structure_conclusion",
            },
            "delivery_pace_filler": {
                "label": "Pace, filler words",
                "max_points": 10,
                "feature_group": "delivery_pace",
            },
            "delivery_eye_facial": {
                "label": "Eye contact, facial expressions",
                "max_points": 10,
                "feature_group": "delivery_conf",
            },
            "delivery_voice": {
                "label": "Voice projection",
                "max_points": 10,
                "feature_group": "delivery_voice",
            },
            "delivery_confidence": {
                "label": "Self-confidence, poise, posture",
                "max_points": 10,
                "feature_group": "delivery_conf",
            },
            "delivery_qa": {
                "label": "Ability to answer questions",
                "max_points": 10,
                "feature_group": "delivery_qa",
            },
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Impromptu Speaking ────────────────────────────────────────────────────
    "ImpromptuSpeaking": {
        "total_points": 100,
        "criteria": {
            "incorporates_topic": {
                "label": "Incorporates provided topic and expands throughout",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "consistent_theme": {
                "label": "Identify and execute a consistent theme",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "supporting_info": {
                "label": "Include accurate supporting information",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "introduction": {
                "label": "Introduce topic immediately (Introduction)",
                "max_points": 10,
                "feature_group": "structure_intro",
            },
            "body": {
                "label": "Support topic throughout (Body)",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "conclusion": {
                "label": "Provide effective conclusion (Closing)",
                "max_points": 10,
                "feature_group": "structure_conclusion",
            },
            "delivery_extemporaneous": {
                "label": "Delivers quality extemporaneous presentation",
                "max_points": 15,
                "feature_group": "delivery_conf",
            },
            "delivery_confidence": {
                "label": "Confidence, body language, eye contact, voice projection",
                "max_points": 15,
                "feature_group": "delivery_conf",
            },
        },
    },
  
    # ── Sales Presentation ────────────────────────────────────────────────────
    "SalesPresentation": {
        "total_points": 110,
        "criteria": {
            "greeting": {
                "label": "Presents appropriate greeting / introduction",
                "max_points": 10,
                "feature_group": "structure_intro",
            },
            "needs_determination": {
                "label": "Able to determine needs",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "product_presentation": {
                "label": "Presenting the product or service",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "overcome_objections": {
                "label": "Able to overcome objections",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "suggestion_selling": {
                "label": "Demonstrates suggestion selling",
                "max_points": 10,
                "feature_group": "content_recommendations",
            },
            "close_sale": {
                "label": "Able to close the sale",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "develop_relationship": {
                "label": "Demonstrates ability to develop relationship",
                "max_points": 10,
                "feature_group": "content_recommendations",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Business Plan ─────────────────────────────────────────────────────────
    "BusinessPlan": {
        "total_points": 85,   # presentation component only (excluding pre-judged report - worth 25 points)
        "criteria": {
            "business_concept": {
                "label": "Describes business concept and company profile",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "marketing": {
                "label": "Explains marketing aspects of business",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "operations_management": {
                "label": "Describes operations and management plans",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "financials": {
                "label": "Provides information on financial documents and projections",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "risks": {
                "label": "Identifies and analyzes risks and adverse results",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "long_term_goals": {
                "label": "Identifies long-term goals",
                "max_points": 10,
                "feature_group": "content_recommendations",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Business Ethics ───────────────────────────────────────────────────────
    "BusinessEthics": {
        "total_points": 95,
        "criteria": {
            "identify_issues": {
                "label": "Identifies and defines ethical issues",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "explains_why": {
                "label": "Explains why the ethical issues happened",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "solutions": {
                "label": "Provides logical recommendations for resolution",
                "max_points": 10,
                "feature_group": "content_recommendations",
            },
            "safeguards": {
                "label": "Recommends safeguards to prevent ethical issues",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "research_accuracy": {
                "label": "Research shows quality and accurate information",
                "max_points": 15,
                "feature_group": "content_accuracy",
            },
            "sources": {
                "label": "Substantiates and cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Data Analysis ─────────────────────────────────────────────────────────
    "DataAnalysis": {
        "total_points": 90,
        "criteria": {
            "topic_understanding": {
                "label": "Demonstrates understanding of event topic",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "data_analysis": {
                "label": "Provides analysis of data",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "visualizations": {
                "label": "Provides visualizations of data (≥3 created by competitor)",
                "max_points": 15,
                "feature_group": "slide_design",
            },
            "recommendations": {
                "label": "Identifies recommendation to accomplish purpose",
                "max_points": 10,
                "feature_group": "content_recommendations",
            },
            "accuracy": {
                "label": "Uses suitable and accurate statements",
                "max_points": 20,
                "feature_group": "content_accuracy",
            },
            "sources": {
                "label": "Substantiates and cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "delivery_organization": {
                "label": "Statements well-organized",
                "max_points": 5,
                "feature_group": "delivery_org",
            },
            "delivery_confidence": {
                "label": "Confidence, body language, eye contact, voice",
                "max_points": 5,
                "feature_group": "delivery_conf",
            },
        },
    },
  
    # ── Financial Planning ────────────────────────────────────────────────────
    "FinancialPlanning": {
        "total_points": 150,
        "criteria": {
            "topic_problem": {
                "label": "Demonstrates understanding of topic and defines problem(s)",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "budgeting": {
                "label": "Explains budgeting and its relation to long-term goals",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "debt_management": {
                "label": "Explains strategies for managing and reducing debt",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "investments_retirement": {
                "label": "Addresses investing vs. saving for retirement",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "goal_attainment": {
                "label": "Recommends steps to achieve financial goals",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "recommendations": {
                "label": "Provides specific financial recommendations",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "professional_guidance": {
                "label": "Identifies relevant financial professionals/services",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Financial Statement Analysis ──────────────────────────────────────────
    "FinancialStatementAnalysis": {
        "total_points": 140,
        "criteria": {
            "describe_statements": {
                "label": "Describes each financial statement and its purpose",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "financial_analysis": {
                "label": "Performs financial analysis of each statement",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "financial_condition": {
                "label": "Describes financial condition using analysis insights",
                "max_points": 15,
                "feature_group": "content_accuracy",
            },
            "guidance": {
                "label": "Offers guidance for business decision making",
                "max_points": 10,
                "feature_group": "content_recommendations",
            },
            "differences": {
                "label": "Highlights key differences vs. prior periods",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "health_analysis": {
                "label": "Analyzes what changes reveal about financial health",
                "max_points": 15,
                "feature_group": "content_accuracy",
            },
            "strategic_decisions": {
                "label": "Recommends 2-3 strategic business decisions backed by analysis",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Supply Chain Management ───────────────────────────────────────────────
    "SupplyChainManagement": {
        "total_points": 120,
        "criteria": {
            "summary": {
                "label": "Summarizes supply chain management scenario and strategy",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "management_planning": {
                "label": "Outlines supply chain structure and operations",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "financial_planning": {
                "label": "Analyzes financial considerations of supply chain strategy",
                "max_points": 20,
                "feature_group": "content_recommendations",
            },
            "demand_planning": {
                "label": "Describes forecasting, demand trends, and decision-making",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Event Planning ────────────────────────────────────────────────────────
    "EventPlanning": {
        "total_points": 180,
        "criteria": {
            "event_overview": {
                "label": "Event overview: purpose, goals, target audience, event type",
                "max_points": 15,
                "feature_group": "content_topic",
            },
            "planning_process": {
                "label": "Planning process: timeline, task assignments, planning meetings",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "budget": {
                "label": "Full income/expense breakdown including donations",
                "max_points": 20,
                "feature_group": "content_accuracy",
            },
            "logistics": {
                "label": "Logistics: venue, vendors, staffing, layout diagrams",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "marketing": {
                "label": "Marketing and promotion: targeted strategies",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "legal_risk": {
                "label": "Legal and risk management: contracts, insurance, permits, safety",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "execution_summary": {
                "label": "Execution summary: date, photos, challenges handled",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "evaluation_reflection": {
                "label": "Evaluation and reflection: attendance data, lessons learned",
                "max_points": 20,
                "feature_group": "content_recommendations",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Introduction to Social Media Strategy ─────────────────────────────────
    "IntroductiontoSocialMediaStrategy": {
        "total_points": 110,
        "criteria": {
            "topic_understanding": {
                "label": "Demonstrates understanding of event topic",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "social_media_strategy": {
                "label": "Demonstrates knowledge of social media strategy and metrics",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "design_development": {
                "label": "Explains the design and development process",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "campaign": {
                "label": "Incorporates campaign into presentation (3 relevant ads, single platform)",
                "max_points": 20,
                "feature_group": "slide_design",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Social Media Strategies ───────────────────────────────────────────────
    "SocialMediaStrategies": {
        "total_points": 110,
        "criteria": {
            "campaign_topic": {
                "label": "Social media campaign effectively addresses the topic for target audience",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "knowledge_metrics": {
                "label": "Demonstrates knowledge of social media strategies and metrics",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "research_methodology": {
                "label": "Describes research, methodology, and design process",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "design_development": {
                "label": "Clearly describes design and development process",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "call_to_action_strategy": {
                "label": "Describes strategies used to create clear call-to-action",
                "max_points": 10,
                "feature_group": "content_recommendations",
            },
            "social_media_posts": {
                "label": "Includes ≥3 social media posts on multiple platforms",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Broadcast Journalism ──────────────────────────────────────────────────
    "BroadcastJournalism": {
        "total_points": 110,
        "criteria": {
            "news_segment": {
                "label": "Broadcast news segment (≤2 min, meets topic requirements)",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "visual_editorial_pre": {
                "label": "Visual and editorial design quality in the segment",
                "max_points": 15,
                "feature_group": "slide_design",
            },
            "visual_editorial_present": {
                "label": "Discusses visual/editorial design choices during presentation",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "production_techniques": {
                "label": "Describes production techniques and tools used",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "research_accuracy_ethics": {
                "label": "Explains research, accuracy, and ethical reporting",
                "max_points": 15,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Digital Video Production ──────────────────────────────────────────────
    "DigitalVideoProduction": {
        "total_points": 90,   # presentation component (excluding pre-judged video - worth 20 points)
        "criteria": {
            "topic_understanding": {
                "label": "Demonstrates understanding of event topic",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "technology_implementation": {
                "label": "Describes use and implementation of innovative technology",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "design_development": {
                "label": "Explains the design and development process",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "incorporates_video": {
                "label": "Incorporates video into presentation with introduction and transition",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            "copyright": {
                "label": "Copyright and source information documented; video is original",
                "max_points": 20,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Digital Animation ─────────────────────────────────────────────────────
    "DigitalAnimation": {
        "total_points": 90,
        "criteria": {
            "topic_understanding": {
                "label": "Demonstrates understanding of event topic",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "development_process": {
                "label": "Describes the development process",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "production_process": {
                "label": "Describes the production process",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "software_hardware": {
                "label": "Describes software and hardware used",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "animation_techniques": {
                "label": "Describes animation techniques used",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "copyright": {
                "label": "Copyright and source information documented; video is original",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Graphic Design ────────────────────────────────────────────────────────
    "GraphicDesign": {
        "total_points": 110,
        "criteria": {
            "event_topic_materials": {
                "label": "Description of event topic and materials, connected pieces",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "design_development": {
                "label": "Explains design and development process (design principles)",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "create_interest": {
                "label": "Creates interest and desire for the design",
                "max_points": 20,
                "feature_group": "slide_design",
            },
            "programs_tools": {
                "label": "Programs/tools used to design graphics",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "theme_consistency": {
                "label": "Consistency in graphic design to theme",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Visual Design ─────────────────────────────────────────────────────────
    "VisualDesign": {
        "total_points": 140,
        "criteria": {
            "event_topic_materials": {
                "label": "Description of event topic and materials, connected pieces",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "design_principles": {
                "label": "Apply design principles (balance, contrast, alignment)",
                "max_points": 20,
                "feature_group": "slide_design",
            },
            "technical_skills": {
                "label": "Demonstrate technical skills: digital tools, formatting",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "communicate_visually": {
                "label": "Design visuals that clearly communicate a message",
                "max_points": 20,
                "feature_group": "slide_design",
            },
            "creative_process": {
                "label": "Explains the creative process (brainstorming, revisions)",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "theme_consistency": {
                "label": "Consistency in graphic design to theme",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Website Design ────────────────────────────────────────────────────────
    "WebsiteDesign": {
        "total_points": 120,
        "criteria": {
            "planning_development": {
                "label": "Describes planning, development, and implementation of project",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "website_features": {
                "label": "Demonstrates required website elements",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "ux_design": {
                "label": "Website UX: color, fonts, graphics, accessibility",
                "max_points": 20,
                "feature_group": "slide_design",
            },
            "grammar_spelling": {
                "label": "Grammar, spelling, punctuation",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            "platform_compatibility": {
                "label": "Compatible with multiple platforms",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "interactivity": {
                "label": "Website interactivity functions, error free",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "consistency": {
                "label": "Website elements consistent across all pages",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "metrics": {
                "label": "Description of metrics planned to measure website success",
                "max_points": 5,
                "feature_group": "content_recommendations",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Website Coding and Development ────────────────────────────────────────
    "WebsiteCodingandDevelopment": {
        "total_points": 220,
        "criteria": {
            "website_coding": {
                "label": "Website coding style (spacing, style sheets, comments)",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "usability_accessibility": {
                "label": "Website usability, accessibility, and navigation",
                "max_points": 20,
                "feature_group": "slide_design",
            },
            "color_contrast_font": {
                "label": "Color/contrast, background, font appropriate for topic",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            "graphics": {
                "label": "Graphics appropriate for topic",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            "topic_coverage": {
                "label": "Fully addresses the topic",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "coding_skills": {
                "label": "Site contains multiple elements evidencing coding skills",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "grammar": {
                "label": "Grammar, spelling, punctuation",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "platform_compatibility": {
                "label": "Compatible with multiple platforms",
                "max_points": 20,
                "feature_group": "slide_design",
            },
            "interactivity": {
                "label": "Interactivity functions, error free",
                "max_points": 20,
                "feature_group": "content_structure",
            },
            "page_consistency": {
                "label": "Website elements consistent across all pages",
                "max_points": 20,
                "feature_group": "slide_design",
            },
            "source_code": {
                "label": "Source code and documentation requirements",
                "max_points": 20,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Coding and Programming ────────────────────────────────────────────────
    "CodingandProgramming": {
        "total_points": 110,
        "criteria": {
            "language_selection": {
                "label": "Coding language selection (detailed explanation using industry terms)",
                "max_points": 5,
                "feature_group": "content_topic",
            },
            "comments_naming": {
                "label": "Appropriate use of comments, naming conventions, formatting",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "modularity": {
                "label": "Program is modular, logical, readable",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "ux_design": {
                "label": "UX Design: user journey, design rationale, accessibility",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            "intuitive_instructions": {
                "label": "User interface intuitive or clear instructions provided",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "navigation": {
                "label": "Users can easily navigate; intelligent feature",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "input_validation": {
                "label": "User input validated (syntactical and semantic)",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            "functionality": {
                "label": "Program addresses all parts of the prompt",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "output_reports": {
                "label": "Program generates presentable, customizable reports",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "data_storage": {
                "label": "Data storage: arrays/lists, variable scope",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Introduction to Programming ───────────────────────────────────────────
    "IntroductiontoProgramming": {
        "total_points": 130,
        "criteria": {
            "comments_naming": {
                "label": "Appropriate use of comments, naming conventions, formatting",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "modularity": {
                "label": "Program is modular, logical, readable",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "intuitive_instructions": {
                "label": "User interface intuitive or clear instructions",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "navigation": {
                "label": "Users can easily navigate; interactive help",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            "input_validation": {
                "label": "User input validated",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            "functionality": {
                "label": "Program fully addresses the prompt",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "output_reports": {
                "label": "Program generates presentable reports",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "data_storage": {
                "label": "Data storage: correct data types, variable scope",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            "documentation": {
                "label": "Comprehensive documentation (readme, source code, attributions)",
                "max_points": 20,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Mobile Application Development ────────────────────────────────────────
    "MobileApplicationDevelopment": {
        "total_points": 110,
        "criteria": {
            "planning_process": {
                "label": "Planning process (tangible planning documents)",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "classes_modules": {
                "label": "Appropriate use of classes, modules, components",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "architectural_patterns": {
                "label": "Appropriate use of mobile app architectural patterns",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "innovation": {
                "label": "Innovation and creativity",
                "max_points": 5,
                "feature_group": "content_topic",
            },
            "ux_design": {
                "label": "UX Design: user journey, design rationale, accessibility",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "intuitive_ui": {
                "label": "User interface intuitive or clear instructions",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "graphics_icons": {
                "label": "Icons/graphical elements appropriate and consistent",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "input_validation": {
                "label": "User input validated",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            "functionality": {
                "label": "Application addresses all parts of prompt",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "social_media_integration": {
                "label": "Integrated with social media",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "data_handling": {
                "label": "Data handling and storage practices",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            "documentation": {
                "label": "Documentation and copyright compliance",
                "max_points": 5,
                "feature_group": "content_accuracy",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Computer Game and Simulation Programming ──────────────────────────────
    "ComputerGameSimulationProgramming": {
        "total_points": 110,
        "criteria": {
            "concept_topic": {
                "label": "Game/simulation addresses all parts of the concept/topic",
                "max_points": 15,
                "feature_group": "content_topic",
            },
            "rules": {
                "label": "Game/simulation rules well-defined and clearly explained",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "challenge_completable": {
                "label": "Game challenging but completable; multiple outcomes",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "innovation_creativity": {
                "label": "Innovation and creativity of game/simulation",
                "max_points": 5,
                "feature_group": "content_topic",
            },
            "implementation": {
                "label": "Programming language, tools, game engines described; complexity evaluated",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            "graphics_assets": {
                "label": "Graphics and game assets appropriate and consistent",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "design_principles": {
                "label": "Color, contrast, typography, sound, design applied",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "title_screen": {
                "label": "Title screen functions and provides clear instructions",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "ux_design": {
                "label": "UX Design: user journey, design rationale, accessibility",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "navigation_engagement": {
                "label": "Users can easily navigate; overall user engagement",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "controls_mechanics": {
                "label": "Game/simulation controls and mechanics are intuitive",
                "max_points": 5,
                "feature_group": "content_structure",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Career Portfolio ──────────────────────────────────────────────────────
    "CareerPortfolio": {
        "total_points": 90,
        "criteria": {
            "resume": {
                "label": "Resume: review of experiences, qualifications, awards, special skills",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "career_research": {
                "label": "Career research: desired career, qualifications correlated",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "career_education": {
                "label": "Career-related education: school activities and work experiences",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "special_skills": {
                "label": "Special skills or proficiencies related to desired career",
                "max_points": 15,
                "feature_group": "content_topic",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "portfolio_use": {
                "label": "Use of portfolio in presentation (enhances presentation)",
                "max_points": 10,
                "feature_group": "slide_design",
            },
            **_DELIVERY_CRITERIA,
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Job Interview ─────────────────────────────────────────────────────────
    "JobInterview": {
        "total_points": 120,
        "criteria": {
            "job_readiness": {
                "label": "Selects a job aligned with qualifications; demonstrates understanding",
                "max_points": 15,
                "feature_group": "content_topic",
            },
            "interview_preparation": {
                "label": "Shows evidence of having researched the company or job",
                "max_points": 15,
                "feature_group": "content_accuracy",
            },
            "response_quality": {
                "label": "Answers questions thoughtfully; problem-solving, self-awareness",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "strengths_experiences": {
                "label": "Articulates relevant skills, experiences, and accomplishments",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "career_goals": {
                "label": "Communicates short- and long-term career goals and enthusiasm",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "greeting_introduction": {
                "label": "Demonstrates proper greeting, introduction, and closing",
                "max_points": 10,
                "feature_group": "structure_intro",
            },
            "confidence_assertiveness": {
                "label": "Demonstrates self-confidence, assertiveness, and enthusiasm",
                "max_points": 15,
                "feature_group": "delivery_conf",
            },
            "verbal_nonverbal": {
                "label": "Demonstrates proper verbal and nonverbal communication skills",
                "max_points": 10,
                "feature_group": "delivery_voice",
            },
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Future Business Leader ────────────────────────────────────────────────
    "FutureBusinessLeader": {
        "total_points": 110,
        "criteria": {
            "fbla_participation": {
                "label": "Illustrates participation and leadership experiences in FBLA",
                "max_points": 15,
                "feature_group": "content_topic",
            },
            "other_organizations": {
                "label": "Explains participation in other school/community organizations",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "outstanding_achievement": {
                "label": "Explains and shows areas of outstanding achievement",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "career_knowledge": {
                "label": "Indicates understanding of career knowledge and plans",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "greeting": {
                "label": "Demonstrates proper greeting, introduction, and closing",
                "max_points": 15,
                "feature_group": "structure_intro",
            },
            "self_confidence": {
                "label": "Demonstrates strong self-confidence, assertiveness, enthusiasm",
                "max_points": 15,
                "feature_group": "delivery_conf",
            },
            "verbal_nonverbal": {
                "label": "Demonstrates proper verbal and nonverbal communication skills",
                "max_points": 10,
                "feature_group": "delivery_voice",
            },
            **_PROTOCOL_CRITERION,
        },
    },
  
    # ── Future Business Educator ──────────────────────────────────────────────
    "FutureBusinessEducator": {
        "total_points": 100,
        "criteria": {
            "subject_matter": {
                "label": "Demonstrated knowledge of subject matter",
                "max_points": 15,
                "feature_group": "content_topic",
            },
            "lesson_objectives": {
                "label": "Presented material met objectives of the lesson plan",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "audience_appropriate": {
                "label": "Presented material appropriate for audience and subject",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "interesting_creative": {
                "label": "Presented interesting, motivating, and creative lesson plan",
                "max_points": 15,
                "feature_group": "content_recommendations",
            },
            "sources": {
                "label": "Cites sources",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "delivery_confidence": {
                "label": "Confidence, body language, eye contact, voice projection",
                "max_points": 10,
                "feature_group": "delivery_conf",
            },
            "verbal_nonverbal": {
                "label": "Proper verbal and nonverbal communication skills",
                "max_points": 10,
                "feature_group": "delivery_voice",
            },
            "delivery_qa": {
                "label": "Ability to effectively answer questions",
                "max_points": 10,
                "feature_group": "delivery_qa",
            },
        },
    },
  
    # ── Public Service Announcement ───────────────────────────────────────────
    "PublicServiceAnnouncement": {
        "total_points": 100,
        "criteria": {
            "learning_objective": {
                "label": "Demonstrates understanding of topic; creates a learning objective",
                "max_points": 10,
                "feature_group": "content_topic",
            },
            "research_findings": {
                "label": "Explains major findings from topic research",
                "max_points": 15,
                "feature_group": "content_accuracy",
            },
            "script": {
                "label": "Describes the design development and script writing process",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "techniques": {
                "label": "Explains video and audio techniques used to create the PSA",
                "max_points": 15,
                "feature_group": "content_structure",
            },
            "equipment_software": {
                "label": "Explains ≥3 types of equipment and/or software used",
                "max_points": 10,
                "feature_group": "content_structure",
            },
            "copyright_sources": {
                "label": "Copyright/source documented; video content is original",
                "max_points": 10,
                "feature_group": "content_accuracy",
            },
            "psa_shown": {
                "label": "PSA video is shown during the presentation",
                "max_points": 5,
                "feature_group": "slide_design",
            },
            "delivery_organization": {
                "label": "Statements well-organized and clearly stated",
                "max_points": 10,
                "feature_group": "delivery_org",
            },
            "delivery_confidence": {
                "label": "Confidence, body language, eye contact, voice projection",
                "max_points": 5,
                "feature_group": "delivery_conf",
            },
            "delivery_qa": {
                "label": "Ability to effectively answer questions",
                "max_points": 10,
                "feature_group": "delivery_qa",
            },
            **_PROTOCOL_CRITERION,
        },
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# 2.  HEURISTIC SCORING FUNCTIONS
#     Each function takes the raw feature values and returns a score in [0, 1],
#     representing the fraction of the max_points for that feature group.
#     The score is later scaled by max_points to get the criterion score.
#
#     Design philosophy (Components D/E):
#       - Use heuristic rules that reflect FBLA rubric structure.
#       - Speaking rate and pausing → delivery/fluency score.
#       - Structural flags (intro/conclusion/recommendations) => organization score.
#       - Slide density => technology/design score.
#       - These heuristics can be replaced with learned models once labeled data
#         is available.
# ──────────────────────────────────────────────────────────────────────────────

def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))

def _score_delivery_pace(
    wpm: float,
    avg_pause_length: float,
    long_pauses_per_minute: float,
) -> float:
  
    """
    Speaking rate and pausing heuristic.
    Research consensus + FBLA rubric language:
      - Ideal WPM for business presentations: ~120-160 wpm.
        Below 100 or above 200 hurts the score.
      - Avg pause length > 1.0 s suggests hesitation; < 0.2 s suggests
        rushing (no natural breath).
      - Long pauses (>= 1 s) per minute: 0-1 is fine, > 3 suggests disfluency.
    Returns a score in [0, 1].
    """
  
    # WPM component (bell curve centered at 140)
    ideal_wpm = 140.0
    sigma_wpm = 35.0
    wpm_score = math.exp(-0.5 * ((wpm - ideal_wpm) / sigma_wpm) ** 2)
  
    # Pause length component
    if avg_pause_length <= 0.2:
        pause_score = 0.6   # too rushed
    elif avg_pause_length <= 0.8:
        pause_score = 1.0   # natural
    elif avg_pause_length <= 1.5:
        pause_score = 0.75  # slightly long
    else:
        pause_score = max(0.3, 1.0 - (avg_pause_length - 1.5) * 0.3)
      
    # Long-pause frequency component
    if long_pauses_per_minute <= 1.0:
        long_pause_score = 1.0
    elif long_pauses_per_minute <= 3.0:
        long_pause_score = 0.7
    else:
        long_pause_score = max(0.2, 1.0 - (long_pauses_per_minute - 3.0) * 0.15)
      
    # Weighted average: wpm 40%, pause length 30%, long-pause freq 30%
    combined = 0.4 * wpm_score + 0.3 * pause_score + 0.3 * long_pause_score
    return _clamp(combined)

def _score_delivery_organization(
    wpm: float,
    has_intro: int,
    has_conclusion: int,
    avg_pause_length: float,
) -> float:
  
    """
    Rubric criterion: 'Statements well-organized and clearly stated.'
    Proxies: intro flag, conclusion flag, and fluent speaking rate.
    """
  
    structure_score = (has_intro + has_conclusion) / 2.0  # 0, 0.5, or 1.0
    fluency_score = _score_delivery_pace(wpm, avg_pause_length, 0.0)
    combined = 0.6 * structure_score + 0.4 * fluency_score
    return _clamp(combined)

def _score_delivery_confidence(
    wpm: float,
    avg_pause_length: float,
    long_pauses_per_minute: float,
) -> float:
    """
    Rubric criterion: 'Confidence, poised body language, engaging eye contact,
    effective voice projection.'
    Proxies from audio: fewer disfluencies and a good pace suggest confidence.
    Eye contact and body language cannot be measured from transcript/audio alone,
    so we use fluency as the best available proxy.
    """
    return _score_delivery_pace(wpm, avg_pause_length, long_pauses_per_minute)

def _score_delivery_qa(
    wpm: float,
    avg_pause_length: float,
) -> float:
    """
    Q&A effectiveness proxy.
    Idea: Q&A is conversational; slightly slower WPM with natural pauses
    suggests thoughtful responses. Pure heuristic - no Q&A transcript available.
    We give a moderate baseline (0.75) as a conservative estimate.
    """
    # We can only weakly proxy this via overall delivery quality.
    pace_score = _score_delivery_pace(wpm, avg_pause_length, 0.0)
    # Blend toward a conservative center so we don't overstate
    return _clamp(0.5 + 0.5 * (pace_score - 0.5))

def _score_content_structure(
    has_intro: int,
    has_conclusion: int,
    has_recommendations: int,
) -> float:
    """
    Rubric criteria related to organization, logical flow, and structure.
    Maps the three binary structural indicators to a score.
    """
    score = (has_intro + has_conclusion + has_recommendations) / 3.0
    return _clamp(score)

def _score_structure_intro(has_intro: int) -> float:
    """Rubric criteria that specifically test for a clear introduction."""
    # 0 => 0.0, 1 => 1.0, but we add a small baseline for partially detected intros
    return _clamp(float(has_intro))

def _score_structure_conclusion(has_conclusion: int) -> float:
    """Rubric criteria that specifically test for an effective conclusion."""
    return _clamp(float(has_conclusion))

def _score_content_recommendations(has_recommendations: int) -> float:
    """
    Rubric criteria that reward recommendations ('identifies recommendations',
    'suggestion selling', 'goal attainment', etc.).
    """
    return _clamp(float(has_recommendations))

def _score_slide_design(
    avg_slide_words: Optional[float],
    slides_per_minute: Optional[float],
) -> float:
    """
    Rubric criterion: 'Technology demonstrates proper formatting, design
    elements, and business presentation features' / 'Clean, professional design.'
    Heuristic (meeting notes, pp.24, 27):
      - avg_slide_words < 20  => 'sparse' (very clean) → high score
      - avg_slide_words 20-50 => 'medium'               → moderate score
      - avg_slide_words > 50  => 'dense'  (text-heavy)  → lower score
    If slide data unavailable, return a conservative neutral estimate.
    """
  
    if avg_slide_words is None:
        return 0.65  # neutral baseline when slides not available
    if avg_slide_words < 15:
        word_score = 0.90
    elif avg_slide_words <= 30:
        word_score = 1.0
    elif avg_slide_words <= 50:
        word_score = 0.75
    elif avg_slide_words <= 80:
        word_score = 0.50
    else:
        word_score = max(0.2, 0.50 - (avg_slide_words - 80) * 0.005)
   
  # slides_per_minute: 1-3 slides/min is typical; too fast or none is bad
    if slides_per_minute is None:
        rate_score = 0.75
    elif slides_per_minute < 0.5:
        rate_score = 0.6   # very few slides
    elif slides_per_minute <= 3.0:
        rate_score = 1.0
    else:
        rate_score = max(0.5, 1.0 - (slides_per_minute - 3.0) * 0.1)
    combined = 0.7 * word_score + 0.3 * rate_score
    return _clamp(combined)

def _score_content_topic(
    wpm: float,
    has_intro: int,
) -> float:
    """
    Proxy for topic understanding / demonstrates knowledge of event topic.
    Without semantic analysis of the transcript, we use delivery quality
    (well-paced speech) and structural clarity (clear intro) as proxies.
    """
    pace = _score_delivery_pace(wpm, 0.5, 1.0)
    return _clamp(0.5 * pace + 0.5 * has_intro)

def _score_content_accuracy(
    has_intro: int,
    has_conclusion: int,
    has_recommendations: int,
) -> float:
    """
    Proxy for 'uses suitable and accurate statements' / 'cites sources'.
    Cannot verify accuracy from audio/transcript alone; use structure as proxy.
    Conservative score skewed slightly high to avoid false penalization.
    """
    structure = (has_intro + has_conclusion + has_recommendations) / 3.0
    return _clamp(0.5 + 0.3 * structure)

def _score_protocol() -> float:
    """
    Protocol adherence is binary (0 or 10 pts) and not derivable from features.
    We assume compliance and return full credit; pipeline can override this to 0
    if a known violation is detected (e.g., time over limit).
    """
    return 1.0

# ──────────────────────────────────────────────────────────────────────────────
# 3.  FEATURE-GROUP → SCORE DISPATCHER
# ──────────────────────────────────────────────────────────────────────────────

def _dispatch_feature_group(
    group: str,
    wpm: float,
    avg_pause_length: float,
    long_pauses_per_minute: float,
    has_intro: int,
    has_conclusion: int,
    has_recommendations: int,
    avg_slide_words: Optional[float],
    slides_per_minute: Optional[float],
) -> float:
    """
    Map a feature_group label to its heuristic score in [0, 1].
    """
    if group == "delivery_org":
        return _score_delivery_organization(wpm, has_intro, has_conclusion, avg_pause_length)
    elif group == "delivery_conf":
        return _score_delivery_confidence(wpm, avg_pause_length, long_pauses_per_minute)
    elif group == "delivery_qa":
        return _score_delivery_qa(wpm, avg_pause_length)
    elif group == "delivery_pace":
        return _score_delivery_pace(wpm, avg_pause_length, long_pauses_per_minute)
    elif group == "delivery_voice":
        return _score_delivery_confidence(wpm, avg_pause_length, long_pauses_per_minute)
    elif group == "content_structure":
        return _score_content_structure(has_intro, has_conclusion, has_recommendations)
    elif group == "structure_intro":
        return _score_structure_intro(has_intro)
    elif group == "structure_conclusion":
        return _score_structure_conclusion(has_conclusion)
    elif group == "content_recommendations":
        return _score_content_recommendations(has_recommendations)
    elif group == "slide_design":
        return _score_slide_design(avg_slide_words, slides_per_minute)
    elif group == "content_topic":
        return _score_content_topic(wpm, has_intro)
    elif group == "content_accuracy":
        return _score_content_accuracy(has_intro, has_conclusion, has_recommendations)
    elif group == "protocol":
        return _score_protocol()
    else:
        return 0.65 # Unknown group: return a neutral score
      
# ──────────────────────────────────────────────────────────────────────────────
# 4.  MAIN SCORING FUNCTION  (Component D + E in the pipeline)
# ──────────────────────────────────────────────────────────────────────────────

def score_presentation(
    event_name: str,
    features: dict,
    protocol_compliant: bool = True,
) -> dict:
    """
    Map low-level features to rubric-aligned criterion scores and compute
    the total rubric score for a given FBLA event.
    Parameters
    ----------
    event_name : str
        One of the keys in EVENTS (e.g. 'IntroductiontoBusinessPresentation').
    features : dict
        Must contain:
          wpm, avg_pause_length, long_pauses_per_minute,
          has_intro, has_conclusion, has_recommendations,
          avg_slide_words (float or None),
          slides_per_minute (float or None, optional).
    protocol_compliant : bool
        Set to False if a known protocol violation was detected.
    Returns
    -------
    dict with keys:
      event           – event name
      total_possible  – maximum rubric points for this event
      criterion_scores – {criterion_key: {"label", "points_earned", "max_points"}}
      total_score     – sum of criterion_scores
      normalized_score – total_score / total_possible * 100  (0-100 scale)
      placement_estimate – dict from Component F
    """
    if event_name not in EVENTS:
        available = sorted(EVENTS.keys())
        raise ValueError(
            f"Unknown event '{event_name}'. Available events:\n"
            + "\n".join(f"  - {e}" for e in available)
        )
      
    event_def = EVENTS[event_name]
    rubric_criteria = event_def["criteria"]
    total_possible = event_def["total_points"]
    wpm = float(features.get("wpm", 130))
    avg_pause_length = float(features.get("avg_pause_length", 0.6))
    long_pauses_per_minute = float(features.get("long_pauses_per_minute", 1.0))
    has_intro = int(features.get("has_intro", 0))
    has_conclusion = int(features.get("has_conclusion", 0))
    has_recommendations = int(features.get("has_recommendations", 0))
    avg_slide_words = features.get("avg_slide_words", None)
    slides_per_minute = features.get("slides_per_minute", None)
    criterion_scores = {}
    total_score = 0.0
    for key, criterion in rubric_criteria.items():
        max_pts = criterion["max_points"]
        group = criterion["feature_group"]
        # Override protocol score based on compliance flag
        if group == "protocol":
            fraction = 1.0 if protocol_compliant else 0.0
        else:
            fraction = _dispatch_feature_group(
                group,
                wpm, avg_pause_length, long_pauses_per_minute,
                has_intro, has_conclusion, has_recommendations,
                avg_slide_words, slides_per_minute,
            )
        points_earned = round(fraction * max_pts, 2)
        criterion_scores[key] = {
            "label": criterion["label"],
            "points_earned": points_earned,
            "max_points": max_pts,
            "fraction": round(fraction, 3),
        }
        total_score += points_earned
    total_score = round(total_score, 2)
    normalized_score = round(total_score / total_possible * 100, 2)
    placement = estimate_placement(event_name, normalized_score)
    return {
        "event": event_name,
        "total_possible": total_possible,
        "total_score": total_score,
        "normalized_score": normalized_score,
        "criterion_scores": criterion_scores,
        "placement_estimate": placement,
    }

# ──────────────────────────────────────────────────────────────────────────────
# 5.  PLACEMENT ESTIMATOR  (Component F in the pipeline)
#     Converts a normalized rubric score to a qualitative placement band.
#
#     Thresholds are heuristic and informed by:
#       - Component F): use rubric ranges and assumptions
#         about how judges separate strong from average performances.
#       - FBLA scoring: total pts vary by event, but normalized to 0-100 the
#         patterns are comparable.
#       - Research on automated scoring of presentations suggests top-tier
#         performers typically cluster in the top 10-15% of scores.
#
#     These thresholds can be tuned once real competition score distributions
#     become available  
# ──────────────────────────────────────────────────────────────────────────────

# Per-event thresholds: (top3_cutoff, top10_cutoff) as normalized 0-100 scores.
# Events with heavier content-analysis rubrics (e.g. Financial Planning) tend
# to have less variability in delivery, so thresholds are slightly lower.
_PLACEMENT_THRESHOLDS: dict[str, tuple[float, float]] = {
    # Presentation events with strong delivery emphasis
    "IntroductiontoBusinessPresentation": (87.0, 75.0),
    "IntroductiontoPublicSpeaking":       (87.0, 75.0),
    "PublicSpeaking":                     (88.0, 76.0),
    "ImpromptuSpeaking":                  (85.0, 73.0),
    "SalesPresentation":                  (86.0, 74.0),
    # Business content events
    "BusinessPlan":                       (85.0, 72.0),
    "BusinessEthics":                     (84.0, 72.0),
    "DataAnalysis":                       (84.0, 72.0),
    "FinancialPlanning":                  (83.0, 71.0),
    "FinancialStatementAnalysis":         (83.0, 71.0),
    "SupplyChainManagement":              (83.0, 71.0),
    "EventPlanning":                      (84.0, 72.0),
    # Marketing / Social media
    "IntroductiontoSocialMediaStrategy":  (85.0, 73.0),
    "SocialMediaStrategies":              (84.0, 72.0),
    # Media / production events
    "BroadcastJournalism":                (84.0, 72.0),
    "DigitalVideoProduction":             (84.0, 72.0),
    "DigitalAnimation":                   (83.0, 71.0),
    "PublicServiceAnnouncement":          (84.0, 72.0),
    # Design events
    "GraphicDesign":                      (85.0, 73.0),
    "VisualDesign":                       (84.0, 72.0),
    # Technology events
    "WebsiteDesign":                      (84.0, 72.0),
    "WebsiteCodingandDevelopment":        (83.0, 71.0),
    "CodingandProgramming":               (83.0, 71.0),
    "IntroductiontoProgramming":          (83.0, 71.0),
    "MobileApplicationDevelopment":       (83.0, 71.0),
    "ComputerGameSimulationProgramming":  (83.0, 71.0),
    # Career / interview events
    "CareerPortfolio":                    (85.0, 73.0),
    "JobInterview":                       (85.0, 73.0),
    "FutureBusinessLeader":               (85.0, 73.0),
    "FutureBusinessEducator":             (84.0, 72.0),
}
_DEFAULT_THRESHOLDS = (85.0, 73.0)

def estimate_placement(event_name: str, normalized_score: float) -> dict:
    """
    Convert a normalized rubric score (0-100) to placement-band estimates.
    Returns
    -------
    dict with:
      top3_likelihood    – 'high' | 'medium' | 'low'
      top10_likelihood   – 'high' | 'medium' | 'low'
      interpretation     – human-readable message (matches Component F output format)
      score_band         – 'Top-3 level' | 'Top-10 but not Top-3' | 'Below Top-10'
    """
    top3_cut, top10_cut = _PLACEMENT_THRESHOLDS.get(event_name, _DEFAULT_THRESHOLDS)
    if normalized_score >= top3_cut:
        top3_likelihood = "high"
        top10_likelihood = "high"
        score_band = "Top-3 level"
        interpretation = (
            f"A predicted score of {normalized_score:.1f}/100 is typically "
            f"consistent with a Top-3-level performance in {event_name}. "
            "The delivery, structure, and design indicators are all in the "
            "strong range."
        )
    elif normalized_score >= top10_cut:
        top3_likelihood = "medium" if normalized_score >= (top3_cut - 5) else "low"
        top10_likelihood = "high"
        score_band = "Top-10 but not Top-3"
        gap = round(top3_cut - normalized_score, 1)
        interpretation = (
            f"A predicted score of {normalized_score:.1f}/100 places this "
            f"presentation in a competitive but not yet Top-3 range for "
            f"{event_name}. A gain of approximately {gap} normalized points "
            "could push it into the Top-3 band."
        )
    elif normalized_score >= top10_cut - 8:
        top3_likelihood = "low"
        top10_likelihood = "medium"
        score_band = "Borderline Top-10"
        interpretation = (
            f"A predicted score of {normalized_score:.1f}/100 is close to "
            f"the Top-10 threshold for {event_name}. Improvements to delivery "
            "fluency, structural clarity, and slide design could shift this "
            "into the competitive range."
        )
    else:
        top3_likelihood = "low"
        top10_likelihood = "low"
        score_band = "Below Top-10"
        interpretation = (
            f"A predicted score of {normalized_score:.1f}/100 appears below "
            f"the Top-10 range for {event_name}. Focus on strengthening the "
            "introduction and conclusion structure, improving speaking pace, "
            "and ensuring explicit recommendations are included."
        )
    return {
        "top3_likelihood": top3_likelihood,
        "top10_likelihood": top10_likelihood,
        "score_band": score_band,
        "interpretation": interpretation,
    }

# ──────────────────────────────────────────────────────────────────────────────
# 6.  FEEDBACK GENERATOR  (Component G)
#     Generates rubric-criterion-specific improvement suggestions,
#     aligned with the FBLA rubric language.
# ──────────────────────────────────────────────────────────────────────────────

_FEEDBACK_TEMPLATES: dict[str, dict[str, str]] = {
    # ── Delivery ──────────────────────────────────────────────────────────────
    "delivery_org": {
        "low":    "Work on structuring your talk with a clear opening, body, and close; "
                  "use signposting phrases ('First, …', 'In conclusion, …') to guide judges.",
        "medium": "The overall flow is mostly logical, but adding explicit transitions "
                  "between sections would make the sequence clearer.",
        "high":   "Statements are well-organized and clearly stated — strong performance.",
    },
    "delivery_conf": {
        "low":    "Practice maintaining steady eye contact and reducing filler words. "
                  "Record yourself to identify hesitation patterns.",
        "medium": "Confidence and body language are adequate; try to eliminate remaining "
                  "filler words and add more vocal variety.",
        "high":   "Confident delivery with strong poise and voice projection.",
    },
    "delivery_qa": {
        "low":    "Prepare for Q&A by anticipating likely judge questions and practicing "
                  "concise, structured answers.",
        "medium": "Q&A responses are generally adequate; aim for more precise, evidence-based answers.",
        "high":   "Q&A handled confidently and accurately.",
    },
    "delivery_pace": {
        "low":    "Your speaking pace is outside the ideal range (≈120-160 wpm). "
                  "Practice with a timer to find a natural, clear cadence.",
        "medium": "Pace is acceptable but could be more consistent; watch for "
                  "stretches that are too fast or too slow.",
        "high":   "Speaking pace and fluency are well-controlled.",
    },
    # ── Content ───────────────────────────────────────────────────────────────
    "content_structure": {
        "low":    "Ensure the presentation includes an explicit intro, a logically "
                  "sequenced body, and a clear conclusion/recommendations.",
        "medium": "Most structural elements are present; tighten the transitions and "
                  "make sure every section connects back to the central purpose.",
        "high":   "Structure and logical flow are strong.",
    },
    "structure_intro": {
        "low":    "Add a clear opening statement in the first 20% of the presentation "
                  "('Today we will…', 'Our topic is…') so judges immediately know the purpose.",
        "medium": "Introduction is present but could be more immediate and purposeful.",
        "high":   "Introduction clearly establishes the purpose right away.",
    },
    "structure_conclusion": {
        "low":    "End with an explicit conclusion phrase ('In summary…', 'To conclude…') "
                  "that wraps back to all key points covered.",
        "medium": "Conclusion exists but could more directly echo the opening purpose.",
        "high":   "Conclusion provides a strong connection to the entire presentation.",
    },
    "content_recommendations": {
        "low":    "Add specific, realistic recommendations ('We recommend that businesses…', "
                  "'Our proposal is…') — this is a heavily-weighted criterion on most FBLA rubrics.",
        "medium": "Recommendations are present; make them more concrete and feasible "
                  "with supporting evidence.",
        "high":   "Recommendations are clear, logical, and well-supported.",
    },
    "content_topic": {
        "low":    "Deepen the topic coverage using industry terminology throughout; "
                  "judges reward evidence that you understand the subject beyond surface level.",
        "medium": "Topic understanding is evident; incorporate more domain-specific "
                  "vocabulary and data to elevate the depth.",
        "high":   "Strong demonstration of topic understanding with industry terminology.",
    },
    "content_accuracy": {
        "low":    "Cite credible, professionally legitimate sources explicitly. "
                  "Every factual claim should be traceable to a named source.",
        "medium": "Some sources are cited; aim for consistent citation of all key data points.",
        "high":   "Compelling evidence from legitimate sources cited throughout.",
    },
    # ── Slides / Design ───────────────────────────────────────────────────────
    "slide_design": {
        "low":    "Reduce text on slides — aim for fewer than 30 words per slide on average. "
                  "Use visuals (charts, images, diagrams) to support your message rather than "
                  "paragraphs of text.",
        "medium": "Slides are mostly clean; ensure design is consistent across all slides "
                  "and that visuals reinforce key points rather than repeat spoken content.",
        "high":   "Slides are professionally designed with clean layouts that support the message.",
    },
    # ── Protocol ──────────────────────────────────────────────────────────────
    "protocol": {
        "low":    "Review the event guidelines carefully. Protocol compliance is binary: "
                  "all checklist items must be met to earn these points.",
        "medium": "Most protocol items met; double-check technology device limits, "
                  "material restrictions, and timing.",
        "high":   "Presentation protocols followed correctly.",
    },
}


def _band(fraction: float) -> str:
    if fraction >= 0.85:
        return "high"
    elif fraction >= 0.65:
        return "medium"
    else:
        return "low"


def generate_feedback(score_result: dict) -> str:
    """
    Generate a structured feedback report from the output of score_presentation().
    Parameters
    ----------
    score_result : dict
        The dict returned by score_presentation().
    Returns
    -------
    str
        A formatted multi-line feedback report.
    """
    event = score_result["event"]
    total = score_result["total_score"]
    possible = score_result["total_possible"]
    norm = score_result["normalized_score"]
    placement = score_result["placement_estimate"]
    criteria = score_result["criterion_scores"]
    lines = [
        "=" * 64,
        f"  FBLA AI Judge — Feedback Report",
        f"  Event: {event}",
        "=" * 64,
        "",
        f"  Estimated Score : {total:.1f} / {possible}  ({norm:.1f} / 100)",
        f"  Placement Band  : {placement['score_band']}",
        f"  Top-3 Outlook   : {placement['top3_likelihood'].upper()}",
        f"  Top-10 Outlook  : {placement['top10_likelihood'].upper()}",
        "",
        f"  {placement['interpretation']}",
        "",
        "─" * 64,
        "  CRITERION BREAKDOWN",
        "─" * 64,
    ]
    for key, c in criteria.items():
        pts = c["points_earned"]
        max_pts = c["max_points"]
        frac = c["fraction"]
        label = c["label"]
        band = _band(frac)
        bar_filled = int(round(frac * 20))
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        lines.append(f"\n  {label}")
        lines.append(f"  [{bar}]  {pts:.1f}/{max_pts}  ({frac*100:.0f}%)")
        # Fetch feedback for the feature group
        group = EVENTS[event]["criteria"][key]["feature_group"]
        tmpl = _FEEDBACK_TEMPLATES.get(group, {})
        suggestion = tmpl.get(band, "")
        if suggestion and band != "high":
            lines.append(f"  ► {suggestion}")
    lines += [
        "",
        "─" * 64,
        "  KEY IMPROVEMENT PRIORITIES",
        "─" * 64,
    ]
    # Sort criteria by fraction ascending and highlight the bottom 3
    sorted_criteria = sorted(
        [(k, v) for k, v in criteria.items()],
        key=lambda x: x[1]["fraction"],
    )
    for key, c in sorted_criteria[:3]:
        group = EVENTS[event]["criteria"][key]["feature_group"]
        tmpl = _FEEDBACK_TEMPLATES.get(group, {})
        suggestion = tmpl.get("low", "")
        lines.append(f"\n  ⚠  {c['label']}: {c['points_earned']:.1f}/{c['max_points']}")
        if suggestion:
            lines.append(f"     {suggestion}")
    lines.append("\n" + "=" * 64)
    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────────────────────
# 7.  QUICK DEMO (run this file directly to verify)
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 64)
    print("  rubric_heuristics.py  —  self-test / demo")
    print("=" * 64)
    # --- Example 1: Strong presentation
    print("\n[Example 1]  Strong presenter — Introduction to Business Presentation")
    strong_features = {
        "wpm": 148,
        "avg_pause_length": 0.55,
        "long_pauses_per_minute": 0.8,
        "has_intro": 1,
        "has_conclusion": 1,
        "has_recommendations": 1,
        "avg_slide_words": 24,
        "slides_per_minute": 1.8,
    }
    result = score_presentation("IntroductiontoBusinessPresentation", strong_features)
    print(f"  Total: {result['total_score']}/{result['total_possible']}  "
          f"({result['normalized_score']:.1f}/100)")
    print(f"  Placement: {result['placement_estimate']['score_band']}")
    print(f"  Top-3: {result['placement_estimate']['top3_likelihood'].upper()}")
    # --- Example 2: Mid-tier presentation
    print("\n[Example 2]  Mid-tier presenter — Public Speaking")
    mid_features = {
        "wpm": 175,
        "avg_pause_length": 1.2,
        "long_pauses_per_minute": 2.5,
        "has_intro": 1,
        "has_conclusion": 0,
        "has_recommendations": 0,
        "avg_slide_words": None,
        "slides_per_minute": None,
    }
    result2 = score_presentation("PublicSpeaking", mid_features)
    print(f"  Total: {result2['total_score']}/{result2['total_possible']}  "
          f"({result2['normalized_score']:.1f}/100)")
    print(f"  Placement: {result2['placement_estimate']['score_band']}")
    print(f"  Top-3: {result2['placement_estimate']['top3_likelihood'].upper()}")
    # --- Example 3: Full feedback report
    print("\n[Example 3]  Full feedback — Sales Presentation")
    sales_features = {
        "wpm": 130,
        "avg_pause_length": 0.7,
        "long_pauses_per_minute": 1.5,
        "has_intro": 1,
        "has_conclusion": 1,
        "has_recommendations": 0,
        "avg_slide_words": 45,
        "slides_per_minute": 2.0,
    }
    result3 = score_presentation("SalesPresentation", sales_features)
    report = generate_feedback(result3)
    print(report)
    # --- Show all available events
    print(f"\n[Info]  {len(EVENTS)} events loaded:")
    for name, ev in sorted(EVENTS.items()):
        ncrit = len(ev["criteria"])
        print(f"  {name:<45}  {ev['total_points']:>4} pts  {ncrit} criteria")
