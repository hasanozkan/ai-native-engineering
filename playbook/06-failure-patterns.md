# 6. Failure patterns

Each of these cost real time before it was written down. They are the
patterns an agent (and a tired human) falls into most.

| Pattern | Symptom | Counter |
|---|---|---|
| **Green but not measuring** | CI passes; the feature is dead | Negative control: make the gate fail once |
| **Zero means "none"** | A search returns nothing, so "it doesn't exist" | Run the same query on something that *does* exist |
| **Inherited red** | A check is red; the change gets blamed | Run the check on `main` first — is the red yours? |
| **Folklore as rule** | "X has no API for that" written into docs | Link the evidence (discovery doc, measured call) or don't write it |
| **Mechanism right, path broken** | Every layer tested; the user path never runs | Test the path the user takes, including the snippet in the docs |
| **Copies of a rule** | The same wrong instruction in ten files | Ask "who owns this rule?" and keep one copy |
| **Reusing a closed card** | New work hides in old history | New problem, new card |
| **Debug works, release doesn't** | Fine in development, broken in the store build | Measure in the production build before calling it done |
| **Formatter as diff noise** | A one-line fix reformats a whole file; review and duplication gates choke | Format only what you changed |
| **Silent chain** | "Released" — from the commit before the fix | Each step checks the previous step's result |
