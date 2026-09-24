---
name: deploy-is-merge
description: GitOps image automation deploys every merge to main; version tags do not deploy
metadata:
  type: reference
---

CI publishes `main-<unix-ts>-<sha>` images on every merge; the image
automation picks the newest and commits the bump to the GitOps repo, which
the cluster reconciles. Evidence of a deploy is that bump commit — not a tag.

Related: [[merges-are-human]]
