import requests
import datetime
import os

# CONFIGURATION
USERNAME = "SidharthxNST"
# Placeholder ASCII art - USER MUST REPLACE THIS
ASCII_ART = r"""
    .g8""bgd
  .dP'     `M
  dM'       `
  MM
  MM.
  `Mb.     ,'
    `"bmmmd'
"""

def fetch_stats(username):
    """Fetches user statistics from GitHub API."""
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # User Info
    user_url = f"https://api.github.com/users/{username}"
    user_resp = requests.get(user_url, headers=headers)
    user_data = user_resp.json()
    
    # Public Repos
    repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    
    # Calculate account age
    created_at = datetime.datetime.strptime(user_data.get("created_at", "2020-01-01T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
    uptime = datetime.datetime.now() - created_at
    years = uptime.days // 365
    months = (uptime.days % 365) // 30
    days = (uptime.days % 365) % 30
    uptime_str = f"{years} years, {months} months, {days} days"

    # Total Stars (Basic approximation)
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_resp = requests.get(repos_url, headers=headers)
    stars = sum(repo["stargazers_count"] for repo in repos_resp.json()) if repos_resp.status_code == 200 else 0

    return {
        "user": username,
        "os": "macOS / Linux / Windows",
        "host": "GitHub Actions",
        "uptime": uptime_str,
        "repos": repos,
        "stars": stars,
        "followers": followers
    }
    
def generate_readme(stats):
    """Generates the README content with the terminal style block."""
    
    # Layout using simple string formatting for the "Neofetch" look
    # We combine ASCII art lines with Info lines
    ascii_lines = ASCII_ART.strip("\n").split("\n")
    
    info_lines = [
        f"{stats['user']}@github",
        "-" * 20,
        f"OS: {stats['os']}",
        f"Host: {stats['host']}",
        f"Uptime: {stats['uptime']}",
        f"IDE: VS Code, Vim",
        "",
        f"Languages: Python, JavaScript, C++, HTML/CSS",
        f"Interests: AI, Full Stack, Competitive Coding",
        "",
        f"Repos: {stats['repos']} | Stars: {stats['stars']}",
        f"Followers: {stats['followers']}",
    ]
    
    # Pad shorter list to match longer list
    max_len = max(len(ascii_lines), len(info_lines))
    ascii_lines += [""] * (max_len - len(ascii_lines))
    info_lines += [""] * (max_len - len(info_lines))
    
    # Combine
    output = "```text\n"
    for ascii_line, info_line in zip(ascii_lines, info_lines):
        # Adjust spacing for alignment
        output += f"{ascii_line:<30}  {info_line}\n"
    output += "```"
    
    return output

if __name__ == "__main__":
    stats = fetch_stats(USERNAME)
    terminal_block = generate_readme(stats)
    
    # Update README
    with open("README.md", "r") as f:
        content = f.read()

    start_marker = "<!-- TERMINAL-STARTS -->"
    end_marker = "<!-- TERMINAL-ENDS -->"
    
    if start_marker in content and end_marker in content:
        new_content = content.split(start_marker)[0] + start_marker + "\n" + terminal_block + "\n" + end_marker + content.split(end_marker)[1]
        
        with open("README.md", "w") as f:
            f.write(new_content)
        print("README.md updated successfully.")
    else:
        print("Markers not found in README.md")
