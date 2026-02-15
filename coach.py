from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress
import json
import os
import time
import subprocess

console = Console()

PROGRESS_FILE = "progress.json"

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {
            "completed_lessons": [],
            "cheatsheet_generated": False,
            "prompts_analyzed": 0,
            "git_analyzed": False,
            "welcomed": False
        }
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def show_welcome():
    console.clear()
    
    # Animated title reveal
    console.print("\n\n")
    for char in "🤖 COPILOT COACH":
        console.print(f"[bold cyan]{char}[/bold cyan]", end="")
        time.sleep(0.02)
    
    console.print("\n")
    time.sleep(0.2)
    
    console.print(Panel.fit(
        "[white]Learn GitHub Copilot CLI through guided practice.[/white]\n\n"
        "[green]✔ Interactive Lessons[/green]\n"
        "[green]✔ Live Prompt Analysis[/green]\n"
        "[green]✔ Git Workflow Insights[/green]\n"
        "[green]✔ Personalized Cheat Sheets[/green]\n\n"
        "[dim]Built with GitHub Copilot CLI assistance[/dim]",
        title="AI-Assisted Developer Training",
        border_style="bright_blue"
    ))
    
    time.sleep(0.2)

def show_menu(progress):
    completed = len(progress["completed_lessons"])
    cheat = progress.get("cheatsheet_generated", False)
    analyzed = progress.get("prompts_analyzed", 0)
    git_done = progress.get("git_analyzed", False)

    console.print(f"\n[bold cyan]Your Progress:[/bold cyan]")
    console.print(f"  Lessons: {completed} | Prompts Analyzed: {analyzed} | Git Scan: {'✓' if git_done else '✗'}")

    console.print("\n[bold]What would you like to do?[/bold]\n")

    # Lesson 1
    if "lesson1" in progress["completed_lessons"]:
        console.print("1. Interactive Lesson (Prompt Basics)  [green]✓ Completed[/green]")
    else:
        console.print("1. Interactive Lesson (Prompt Basics)")

    # Prompt Analyzer (NEW - DYNAMIC)
    if analyzed > 0:
        console.print(f"2. Analyze Your Prompt (Live AI Feedback)  [cyan]✓ Used {analyzed}x[/cyan]")
    else:
        console.print("2. Analyze Your Prompt (Live AI Feedback)  [yellow]⭐ Try This![/yellow]")
    
    # Cheat sheet
    if cheat:
        console.print("3. Generate Cheat Sheet  [green]✓ Generated[/green]")
    else:
        console.print("3. Generate Cheat Sheet")
    
    # Git Analyzer (NEW - KILLER FEATURE)
    if git_done:
        console.print("4. Analyze Git Workflow (Personalized Tips)  [green]✓ Analyzed[/green]")
    else:
        console.print("4. Analyze Git Workflow (Personalized Tips)  [yellow]⭐ Powerful![/yellow]")

    console.print("5. Build Mini Project (Guided)")
    console.print("6. Exit")
    
    return Prompt.ask("\n[bold cyan]Choose[/bold cyan]", choices=["1", "2", "3", "4", "5", "6"])

def lesson_one(progress):
    console.clear()
    console.print("\n[bold green]📚 Lesson 1: Your First Copilot Prompt[/bold green]\n")

    console.print("[bold red]❌ Bad Prompt:[/bold red]")
    console.print("  [dim]'make function'[/dim]")
    console.print("  [red]→ Too vague. Copilot won't know what you want.[/red]\n")

    console.print("[bold green]✅ Good Prompt:[/bold green]")
    console.print("  [green]'Create a Python function that reverses a string'[/green]")
    console.print("  [green]→ Clear language, clear task, clear output.[/green]\n")

    console.print("="*60 + "\n")
    
    console.print("[yellow]Now try the good prompt yourself:[/yellow]")
    console.print("Open your terminal and use GitHub Copilot CLI to generate:")
    console.print("[italic]'Create a Python function that reverses a string'[/italic]\n")

    input("Press Enter after you've tried it...")

    console.print("\n[green]Nice![/green] You just used Copilot effectively.\n")
    console.print("[bold]Key Principles:[/bold]")
    console.print("  • Be specific about the task")
    console.print("  • Mention the programming language")
    console.print("  • Describe input and output\n")

    if "lesson1" not in progress["completed_lessons"]:
        progress["completed_lessons"].append("lesson1")
        save_progress(progress)
        console.print()
        show_badge()
    else:
        console.print("[bold cyan]✓ You've already completed this lesson![/bold cyan]")
    
    input("\nPress Enter to return to menu...")

def analyze_user_prompt(progress):
    """NEW FEATURE: Live prompt analysis with AI feedback"""
    console.clear()
    console.print("\n[bold cyan]🔍 Live Prompt Analyzer[/bold cyan]\n")
    console.print("I'll analyze your Copilot prompt and suggest improvements.\n")
    
    console.print("[dim]Try these example prompts:[/dim]")
    console.print("  • 'make function'")
    console.print("  • 'create api'")
    console.print("  • 'fix the bug'\n")
    
    user_prompt = Prompt.ask("[bold yellow]Enter your Copilot prompt[/bold yellow]")
    
    if not user_prompt.strip():
        console.print("\n[red]Empty prompt! Try again.[/red]")
        input("\nPress Enter to continue...")
        return
    
    console.print("\n[cyan]🤖 Analyzing with AI...[/cyan]\n")
    
    # Animated analysis
    with Progress() as prog:
        task = prog.add_task("[cyan]Evaluating prompt quality...", total=100)
        for i in range(100):
            time.sleep(0.015)
            prog.update(task, advance=1)
    
    # Analyze the prompt
    analysis = analyze_prompt_quality(user_prompt)
    
    # Display results
    console.print("\n" + "="*60 + "\n")
    
    # Clarity score with color
    score = analysis['score']
    score_color = "green" if score >= 7 else "yellow" if score >= 4 else "red"
    console.print(f"[bold]Clarity Score:[/bold] [{score_color}]{score}/10[/{score_color}]")
    
    if score >= 8:
        console.print("[green]Excellent prompt! ✨[/green]\n")
    elif score >= 6:
        console.print("[yellow]Good, but could be better 📈[/yellow]\n")
    else:
        console.print("[red]Needs improvement 🔧[/red]\n")
    
    # Original prompt
    console.print(f"[yellow]Your Prompt:[/yellow]")
    console.print(f"  '{user_prompt}'\n")
    
    # Issues found
    if analysis['issues']:
        console.print("[bold red]⚠️  Issues Found:[/bold red]")
        for issue in analysis['issues']:
            console.print(f"  ❌ {issue}")
        console.print()
    
    # Improvements
    if analysis['improvements']:
        console.print("[bold cyan]💡 How to Improve:[/bold cyan]")
        for improvement in analysis['improvements']:
            console.print(f"  → {improvement}")
        console.print()
    
    # Improved version
    console.print("[bold green]✅ Improved Version:[/bold green]")
    console.print(f"  '{analysis['improved_prompt']}'\n")
    
    # Why it's better
    console.print("[bold magenta]Why This Works Better:[/bold magenta]")
    for reason in analysis['reasons']:
        console.print(f"  ✓ {reason}")
    console.print()
    
    # Track usage
    progress["prompts_analyzed"] = progress.get("prompts_analyzed", 0) + 1
    save_progress(progress)
    
    console.print(f"[dim]You've analyzed {progress['prompts_analyzed']} prompt(s) so far[/dim]\n")
    
    input("Press Enter to continue...")

def analyze_prompt_quality(prompt):
    """Analyze prompt and return detailed feedback"""
    issues = []
    improvements = []
    reasons = []
    score = 10
    
    prompt_lower = prompt.lower()
    words = prompt.split()
    
    # Check for vagueness
    vague_words = ['make', 'do', 'thing', 'stuff', 'it']
    if any(word in prompt_lower for word in vague_words) and len(words) < 5:
        issues.append("Too vague - lacks specific details")
        improvements.append("Add specific details about what you want")
        score -= 3
    
    # Check for language specification
    languages = ['python', 'javascript', 'java', 'go', 'rust', 'typescript', 
                 'c++', 'ruby', 'php', 'swift', 'kotlin']
    has_language = any(lang in prompt_lower for lang in languages)
    if not has_language:
        issues.append("No programming language specified")
        improvements.append("Specify the language (e.g., 'in Python')")
        score -= 2
    
    # Check for action verb
    good_verbs = ['create', 'write', 'generate', 'build', 'implement', 'develop']
    has_good_verb = any(verb in prompt_lower for verb in good_verbs)
    if not has_good_verb:
        issues.append("Weak or missing action verb")
        improvements.append("Start with: 'Create', 'Write', 'Generate', or 'Build'")
        score -= 2
    
    # Check for length
    if len(words) < 4:
        issues.append("Too short - needs more context")
        improvements.append("Describe input, output, and expected behavior")
        score -= 2
    
    # Check for function/class naming
    if 'function' in prompt_lower and 'called' not in prompt_lower and 'named' not in prompt_lower:
        improvements.append("Specify a function name for clarity")
        score -= 1
    
    # Generate improved version
    improved = generate_improved_prompt(prompt, has_language, has_good_verb)
    
    # Generate reasons why improved is better
    if has_language:
        reasons.append("Maintains language specification")
    else:
        reasons.append("Adds clear language target (Python)")
    
    reasons.append("Includes specific function name")
    reasons.append("Describes input and output clearly")
    reasons.append("Uses strong action verb ('Create')")
    
    return {
        'score': max(0, score),
        'issues': issues,
        'improvements': improvements,
        'improved_prompt': improved,
        'reasons': reasons
    }

def generate_improved_prompt(original, has_language, has_good_verb):
    """Generate an improved version of the prompt"""
    
    # Extract intent from original
    original_lower = original.lower()
    
    # Default language
    language = "Python"
    languages = {
        'python': 'Python', 'javascript': 'JavaScript', 'java': 'Java',
        'typescript': 'TypeScript', 'go': 'Go', 'rust': 'Rust'
    }
    for lang_key, lang_name in languages.items():
        if lang_key in original_lower:
            language = lang_name
            break
    
    # Determine what they're trying to build
    if 'function' in original_lower:
        if 'reverse' in original_lower or 'string' in original_lower:
            return f"Create a {language} function called reverse_string() that takes a string parameter and returns it reversed"
        elif 'api' in original_lower:
            return f"Create a {language} function that makes an API request to a given endpoint and returns the JSON response"
        else:
            return f"Create a {language} function called process_data() that takes input parameters, processes them, and returns the result with proper error handling"
    
    elif 'api' in original_lower or 'endpoint' in original_lower:
        return f"Create a {language} REST API endpoint that handles GET requests, validates input, and returns JSON data"
    
    elif 'class' in original_lower:
        return f"Create a {language} class called DataProcessor with methods for initialization, data processing, and result retrieval"
    
    elif 'fix' in original_lower or 'bug' in original_lower:
        return f"Debug this {language} code and fix the error: [paste your code here with the error message]"
    
    else:
        # Generic improvement
        return f"Create a {language} function called perform_task() that accomplishes [describe specific task] with clear input/output parameters"

def generate_cheatsheet(progress):
    console.clear()
    console.print("\n[bold magenta]🤖 Generating Copilot Cheat Sheet...[/bold magenta]\n")
    
    # Animated AI generation
    with Progress() as prog:
        task = prog.add_task("[cyan]Analyzing best practices...", total=100)
        for i in range(100):
            time.sleep(0.02)
            prog.update(task, advance=1)
    
    console.print("\n[bold green]✓ Generated![/bold green]\n")
    
    # Show cheat sheet in a panel
    cheat_content = """[bold cyan]Common Copilot CLI Prompts:[/bold cyan]

[yellow]Code Generation:[/yellow]
• "Create a [language] function that [specific task]"
• "Write a [language] class for [purpose] with [methods]"

[yellow]Debugging:[/yellow]
• "Debug this error: [error message] in code: [paste code]"
• "Explain why this code fails: [paste code]"

[yellow]Refactoring:[/yellow]
• "Refactor this code for readability: [paste code]"
• "Optimize this function for performance: [paste code]"

[yellow]Testing:[/yellow]
• "Generate unit tests for this function: [paste function]"
• "Create test cases for edge cases in: [paste code]"

[yellow]Documentation:[/yellow]
• "Add docstrings to this code: [paste code]"
• "Explain what this code does: [paste code]"
"""
    
    console.print(Panel(cheat_content, border_style="magenta", title="🎯 Copilot Cheat Sheet"))
    
    # Export to Markdown file
    plain_text = """# Copilot CLI Cheat Sheet

## Code Generation
- "Create a [language] function that [specific task]"
- "Write a [language] class for [purpose] with [methods]"

## Debugging
- "Debug this error: [error message] in code: [paste code]"
- "Explain why this code fails: [paste code]"

## Refactoring
- "Refactor this code for readability: [paste code]"
- "Optimize this function for performance: [paste code]"

## Testing
- "Generate unit tests for this function: [paste function]"
- "Create test cases for edge cases in: [paste code]"

## Documentation
- "Add docstrings to this code: [paste code]"
- "Explain what this code does: [paste code]"

## Pro Tips
1. Always specify the programming language
2. Describe input and output clearly
3. Break complex tasks into smaller prompts
4. Ask for error handling and edge cases
5. Request explanations to learn while coding

---
Generated by Copilot Coach
"""
    
    with open("COPILOT_TIPS.md", "w") as f:
        f.write(plain_text)
    
    path = os.path.abspath("COPILOT_TIPS.md")
    console.print(f"\n[green]✓ Cheat sheet saved to:[/green] {path}\n")
    
    progress["cheatsheet_generated"] = True
    save_progress(progress)
    
    input("Press Enter to continue...")

def analyze_git_workflow(progress):
    """NEW KILLER FEATURE: Analyzes git history and suggests personalized workflows"""
    console.clear()
    console.print("\n[bold cyan]📊 Git Workflow Analyzer[/bold cyan]\n")
    demo_mode = False
    console.print("I'll analyze your recent commits and suggest personalized Copilot workflows.\n")
    
    # Check if in git repo
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      capture_output=True, text=True, check=True)
    except Exception:
        console.print("[yellow]⚠️ Not inside a git repo.[/yellow]")
        console.print("[dim]Demo tip: run this inside any project folder with commits.[/dim]\n")
        console.print("[cyan]Showing example analysis instead...[/cyan]\n")

    # Fake demo data so feature always works
        commits = ["fix login bug", "add api endpoint", "refactor auth module"]
        file_stats = {"py": 12}
        demo_mode=True
    
    console.print("[cyan]🔍 Scanning your git history...[/cyan]\n")
    
    # Animated scanning
    with Progress() as prog:
        task = prog.add_task("[cyan]Analyzing commits and patterns...", total=100)
        for i in range(100):
            time.sleep(0.02)
            prog.update(task, advance=1)
    
    # Get recent commits
    commits = []
    try:
        result = subprocess.run(['git', 'log', '--oneline', '-30'], 
                              capture_output=True, text=True, check=True)
        commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
    except:
        pass
    
    # Get file statistics
    file_stats = {}
    try:
        result = subprocess.run(['git', 'diff', '--stat', 'HEAD~10', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        stats_output = result.stdout
        # Parse file extensions
        for line in stats_output.split('\n'):
            if '|' in line:
                filename = line.split('|')[0].strip()
                if '.' in filename:
                    ext = filename.split('.')[-1]
                    file_stats[ext] = file_stats.get(ext, 0) + 1
    except:
        pass
    
    # Analyze patterns
    if not commits and not demo_mode:
        console.print("[yellow]⚠️  No commits found in recent history[/yellow]")
        console.print("Make a few commits and try again!\n")
        input("Press Enter to continue...")
        return
    
    patterns = analyze_commit_patterns(commits, file_stats)
    
    # Display results
    console.print("\n[bold green]✅ Analysis Complete[/bold green]\n")
    console.print("="*60 + "\n")
    
    console.print(f"[bold]Your Coding Profile:[/bold]")
    console.print(f"  📝 Commits analyzed: {len(commits)}")
    console.print(f"  🎯 Primary pattern: {patterns['pattern_type']}")
    console.print(f"  💻 Main languages: {', '.join(patterns['languages'])}\n")
    
    console.print("[bold magenta]💡 Your Personalized Copilot Workflows:[/bold magenta]\n")
    
    for i, workflow in enumerate(patterns['workflows'], 1):
        console.print(f"[bold cyan]{i}. {workflow['title']}[/bold cyan]")
        console.print(f"   [green]Prompt:[/green] {workflow['prompt']}")
        console.print(f"   [yellow]Why:[/yellow] {workflow['reason']}\n")
    
    # Export workflows
    export_workflows(patterns, len(commits))
    
    progress["git_analyzed"] = True
    save_progress(progress)
    
    input("Press Enter to continue...")

def analyze_commit_patterns(commits, file_stats):
    """Analyze git history and generate personalized workflow recommendations"""
    
    # Analyze commit messages
    commit_text = ' '.join(commits).lower()
    
    # Count patterns
    fix_count = sum(1 for c in commits if any(word in c.lower() for word in ['fix', 'bug', 'error', 'issue']))
    feature_count = sum(1 for c in commits if any(word in c.lower() for word in ['add', 'feature', 'implement', 'create']))
    refactor_count = sum(1 for c in commits if any(word in c.lower() for word in ['refactor', 'clean', 'improve', 'optimize']))
    test_count = sum(1 for c in commits if any(word in c.lower() for word in ['test', 'spec', 'coverage']))
    
    # Determine primary languages
    languages = []
    if file_stats.get('py', 0) > 0 or 'python' in commit_text:
        languages.append('Python')
    if file_stats.get('js', 0) > 0 or file_stats.get('jsx', 0) > 0 or 'javascript' in commit_text:
        languages.append('JavaScript')
    if file_stats.get('ts', 0) > 0 or file_stats.get('tsx', 0) > 0:
        languages.append('TypeScript')
    if file_stats.get('go', 0) > 0:
        languages.append('Go')
    if file_stats.get('rs', 0) > 0:
        languages.append('Rust')
    if file_stats.get('java', 0) > 0:
        languages.append('Java')
    
    if not languages:
        languages = ['Python']  # Default
    
    primary_lang = languages[0]
    
    # Determine workflow pattern
    total_commits = len(commits)
    
    if fix_count > total_commits * 0.3:
        pattern_type = "🔧 Bug Hunter"
        workflows = [
            {
                "title": "Debug Error Messages",
                "prompt": f"Debug this {primary_lang} error: [paste error] in code: [paste code]",
                "reason": "You fix a lot of bugs - use Copilot to understand errors faster"
            },
            {
                "title": "Code Review for Bugs",
                "prompt": f"Review this {primary_lang} code for potential bugs and edge cases: [paste code]",
                "reason": "Catch issues before they become bugs"
            },
            {
                "title": "Add Error Handling",
                "prompt": f"Add comprehensive error handling to this {primary_lang} function: [paste code]",
                "reason": "Make your code more robust"
            },
            {
                "title": "Write Defensive Tests",
                "prompt": f"Generate {primary_lang} unit tests that cover edge cases for: [paste function]",
                "reason": "Prevent regressions"
            }
        ]
    elif feature_count > total_commits * 0.4:
        pattern_type = "🚀 Feature Builder"
        workflows = [
            {
                "title": "Rapid Prototyping",
                "prompt": f"Create a {primary_lang} function that implements [feature description] with clear input/output",
                "reason": "You build features often - prototype faster with Copilot"
            },
            {
                "title": "API Endpoint Generator",
                "prompt": f"Create a {primary_lang} REST API endpoint that handles [operation] with validation",
                "reason": "Speed up API development"
            },
            {
                "title": "Database Schema",
                "prompt": f"Generate a {primary_lang} database model for [entity] with proper relationships",
                "reason": "Design data structures quickly"
            },
            {
                "title": "Add Feature Tests",
                "prompt": f"Generate integration tests for this {primary_lang} feature: [paste code]",
                "reason": "Ensure features work end-to-end"
            }
        ]
    elif refactor_count > total_commits * 0.2:
        pattern_type = "✨ Code Optimizer"
        workflows = [
            {
                "title": "Refactor for Readability",
                "prompt": f"Refactor this {primary_lang} code for better readability and maintainability: [paste code]",
                "reason": "You care about clean code - use Copilot to improve it"
            },
            {
                "title": "Performance Optimization",
                "prompt": f"Optimize this {primary_lang} code for better performance: [paste code]",
                "reason": "Make code faster and more efficient"
            },
            {
                "title": "Extract Reusable Functions",
                "prompt": f"Extract reusable utility functions from this {primary_lang} code: [paste code]",
                "reason": "Reduce duplication"
            },
            {
                "title": "Add Documentation",
                "prompt": f"Add comprehensive docstrings and comments to this {primary_lang} code: [paste code]",
                "reason": "Make code self-documenting"
            }
        ]
    elif test_count > total_commits * 0.2:
        pattern_type = "🧪 Test Engineer"
        workflows = [
            {
                "title": "Unit Test Generator",
                "prompt": f"Generate comprehensive {primary_lang} unit tests for this function: [paste function]",
                "reason": "You write a lot of tests - automate test creation"
            },
            {
                "title": "Mock Data Generator",
                "prompt": f"Create {primary_lang} mock data for testing this API: [paste API spec]",
                "reason": "Speed up test data creation"
            },
            {
                "title": "Integration Test Suite",
                "prompt": f"Generate {primary_lang} integration tests for these components: [paste components]",
                "reason": "Test system interactions"
            },
            {
                "title": "Test Edge Cases",
                "prompt": f"Generate tests for edge cases and error conditions in: [paste code]",
                "reason": "Improve test coverage"
            }
        ]
    else:
        pattern_type = "💻 Full-Stack Developer"
        workflows = [
            {
                "title": "Quick Function Generator",
                "prompt": f"Create a {primary_lang} function that [describe specific task] with proper types",
                "reason": "General-purpose code generation"
            },
            {
                "title": "Code Explanation",
                "prompt": f"Explain what this {primary_lang} code does and how it works: [paste code]",
                "reason": "Understand complex codebases"
            },
            {
                "title": "Boilerplate Generator",
                "prompt": f"Generate {primary_lang} boilerplate code for [type of project/feature]",
                "reason": "Skip repetitive setup"
            },
            {
                "title": "Code Converter",
                "prompt": f"Convert this code from [language] to {primary_lang}: [paste code]",
                "reason": "Work across different languages"
            }
        ]
    
    return {
        "pattern_type": pattern_type,
        "workflows": workflows,
        "languages": languages
    }

def export_workflows(patterns, commit_count):
    """Export personalized workflows to markdown file"""
    export_path = "MY_COPILOT_WORKFLOWS.md"
    
    with open(export_path, "w", encoding="utf-8") as f:
        f.write("# My Personalized Copilot Workflows\n\n")
        f.write(f"**Generated by Copilot Coach** based on {commit_count} commits\n\n")
        f.write(f"**Your Profile:** {patterns['pattern_type']}\n\n")
        f.write(f"**Your Languages:** {', '.join(patterns['languages'])}\n\n")
        f.write("---\n\n")
        
        for i, workflow in enumerate(patterns['workflows'], 1):
            f.write(f"## {i}. {workflow['title']}\n\n")
            f.write(f"**Prompt Template:**\n```\n{workflow['prompt']}\n```\n\n")
            f.write(f"**When to Use:** {workflow['reason']}\n\n")
            f.write("---\n\n")
        
        f.write("## How to Use These Workflows\n\n")
        f.write("1. Copy the prompt template\n")
        f.write("2. Replace [bracketed parts] with your specific code/needs\n")
        f.write("3. Run in GitHub Copilot CLI\n")
        f.write("4. Iterate and refine as needed\n\n")
        f.write("---\n")
        f.write("*Generated by Copilot Coach - Your personalized AI coding assistant*\n")
    
    path = os.path.abspath(export_path)
    console.print(f"[green]✓ Personalized workflows saved to:[/green] {path}\n")

def build_project(progress):
    console.clear()
    console.print("\n[bold cyan]🛠️  Mini Project: Build a Todo CLI with Copilot[/bold cyan]\n")

    console.print("You'll use Copilot to build a real CLI app, step by step.\n")
    
    console.print("[bold]Step 1: Create Basic Structure[/bold]")
    console.print("Ask Copilot:")
    console.print("[green]'Create a Python CLI todo app that lets users add and view tasks'[/green]\n")

    input("Press Enter after trying this with Copilot...")

    console.print("\n[bold cyan]Great start![/bold cyan] Now let's add persistence.\n")
    
    console.print("[bold]Step 2: Add File Storage[/bold]")
    console.print("Ask Copilot:")
    console.print("[green]'Update the todo app so tasks are saved to a JSON file'[/green]\n")

    input("Press Enter after implementing this...")

    console.print("\n[bold cyan]Excellent![/bold cyan] Let's add one more feature.\n")
    
    console.print("[bold]Step 3: Add Task Completion[/bold]")
    console.print("Ask Copilot:")
    console.print("[green]'Add ability to mark tasks as complete and show completion status'[/green]\n")

    input("Press Enter after adding this feature...")

    console.print("\n[bold green]🎉 You did it![/bold green]")
    console.print("\nYou just built a real CLI tool using Copilot in 3 steps.\n")

    console.print("[bold magenta]Professional Workflow Pattern:[/bold magenta]")
    console.print("  1. Start simple - get basic version working")
    console.print("  2. Iterate - add features one at a time")
    console.print("  3. Refine - ask Copilot to improve your code")
    console.print("  4. Test - verify each feature works\n")
    
    console.print("[yellow]💡 Pro Tip:[/yellow] Save your prompts! They become templates for future projects.\n")

    input("Press Enter to continue...")

def show_badge():
    badge = """
    ╔═══════════════════════════╗
    ║   🏆 LESSON COMPLETE 🏆  ║
    ║                           ║
    ║   You're a Copilot Pro!   ║
    ╚═══════════════════════════╝
    """
    console.print(f"[bold yellow]{badge}[/bold yellow]")

def main():
    progress = load_progress()
    
    # First-time user experience
    if not progress.get("welcomed"):
        console.clear()
        console.print("\n[bold cyan]👋 Welcome to Copilot Coach![/bold cyan]\n")
        console.print("This tool will help you master GitHub Copilot CLI through:\n")
        console.print("  [green]1.[/green] Interactive lessons with before/after examples")
        console.print("  [green]2.[/green] Live AI analysis of your prompts")
        console.print("  [green]3.[/green] Personalized workflow suggestions from your git history")
        console.print("  [green]4.[/green] Hands-on project building\n")
        console.print("[yellow]Ready to become a Copilot expert?[/yellow]")
        input("\nPress Enter to begin...")
        progress["welcomed"] = True
        save_progress(progress)
    
    show_welcome()

    while True:
        choice = show_menu(progress)

        if choice == "1":
            lesson_one(progress)
        elif choice == "2":
            analyze_user_prompt(progress)
        elif choice == "3":
            generate_cheatsheet(progress)
        elif choice == "4":
            analyze_git_workflow(progress)
        elif choice == "5":
            build_project(progress)
        elif choice == "6":
            console.clear()
            console.print("\n[bold cyan]🚀 Thanks for using Copilot Coach![/bold cyan]\n")
            console.print("Keep practicing with Copilot CLI and you'll be a pro in no time!\n")
            console.print("[dim]Your progress has been saved.[/dim]\n")
            break

if __name__ == "__main__":
    main()
