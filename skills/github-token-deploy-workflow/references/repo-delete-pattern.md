# Repo Deletion via GitHub API — Correct Pattern

When deleting a repo via `DELETE /repos/{owner}/{repo}`, the response is **204 No Content with an EMPTY body**. Do NOT try to `json.load()` the response — it will raise `JSONDecodeError: Expecting value`.

## Correct Pattern

```bash
# Step 1: DELETE — capture HTTP status code, ignore body
curl -s -o /dev/null -w "DELETE:%{http_code}\n" -X DELETE \
  -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO"
# Expect: DELETE:204

# Step 2: Confirm with GET — the 404 is the REAL proof
sleep 2
curl -s -o /dev/null -w "GET:%{http_code}\n" \
  -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO"
# Expect: GET:404
```

## Why Both Steps

- 204 = "request succeeded, no body returned" — could theoretically succeed but repo still exists (edge cases)
- 404 = "resource not found" — definitive proof deletion propagated

Always report both codes: `DELETE:204, GET:404` = fully deleted.

## In Python (if needed)

```python
import requests

# DELETE
resp = requests.delete(f"https://api.github.com/repos/{owner}/{repo}",
                       headers={"Authorization": f"token {GH_TOKEN}"})
assert resp.status_code == 204, f"DELETE failed: {resp.status_code}"

# Confirm GET
resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}",
                    headers={"Authorization": f"token {GH_TOKEN}"})
assert resp.status_code == 404, f"GET after DELETE not 404: {resp.status_code}"
```

## Common Mistake

```python
# WRONG — fails because 204 returns empty string
resp = requests.delete(...)
data = resp.json()  # JSONDecodeError
```