---
description: How to push the local repository to GitHub
---

1.  **Create a Repository on GitHub**
    *   Go to [github.com/new](https://github.com/new).
    *   Name it `silicon-colosseum` (or whatever you prefer).
    *   **Do not** initialize with README, .gitignore, or license (we already have them).
    *   Click "Create repository".

2.  **Link Local Repository to GitHub**
    *   Copy the URL of your new repository (e.g., `https://github.com/username/silicon-colosseum.git`).
    *   Run the following command in your terminal (replace the URL):
        ```powershell
        git remote add origin https://github.com/YOUR_USERNAME/silicon-colosseum.git
        ```

3.  **Push the Code**
    *   Push your changes to the main branch:
        ```powershell
        git branch -M main
        git push -u origin main
        ```
