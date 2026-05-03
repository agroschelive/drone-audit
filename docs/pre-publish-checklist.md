# Pre-publish checklist

Before the first public push:

- [ ] Confirm that `agroschelive@gmail.com` is the correct public contact for project security and communication.
- [ ] Run `PYTHONPATH=src pytest -q`.
- [ ] Check `git status`.
- [ ] Search for secrets.
- [ ] Confirm that examples are fictitious.
- [ ] Confirm that no real flight file was included.
- [ ] Confirm that no PDF, report, proposal or commercial data was included.
- [ ] Confirm that `.env` does not exist in the commit.
- [ ] Confirm that there is no previous Git history with sensitive data.
- [ ] Enable Secret Scanning and Push Protection on GitHub when available.
