import os
import argparse

MODULES = {
    "module-2-digital-twin": [
        "week-5-gazebo-basics",
        "week-6-unity-robotics",
        "week-7-sim-to-real"
    ],
    "module-3-nvidia-isaac": [
        "week-8-isaac-sim-intro",
        "week-9-isaac-ros-bridge",
        "week-10-advanced-simulation"
    ],
    "module-4-vla": [
        "week-11-vla-architecture",
        "week-12-training-vla",
        "week-13-deploying-humanoids"
    ]
}

def generate_chapters(base_dir="frontend/docs"):
    for module, weeks in MODULES.items():
        module_path = os.path.join(base_dir, module)
        os.makedirs(module_path, exist_ok=True)
        for week in weeks:
            file_path = os.path.join(module_path, f"{week}.md")
            if not os.path.exists(file_path):
                title = week.replace("-", " ").title()
                content = f"""# {title}

## Introduction

Welcome to {title}. This chapter covers the essential concepts of this topic.

## Content

(Draft content to be expanded...)
"""
                with open(file_path, "w") as f:
                    f.write(content)
                print(f"Created: {file_path}")

if __name__ == "__main__":
    generate_chapters()
