# NFS Raider v2.0

NFS Raider v2.0 is a modern, standalone hash inspection and resolution tool for
Need for Speed (Black Box engine titles).

It is designed to behave like OGVI / Attribulator Raider while providing a
cleaner UI, real-time hash resolution, and full BIN + VLT domain visibility.

---
![image_alt](https://github.com/CiPH3R-88/NFS_Raider_v2.0/blob/377d983f12444ab24eb4ef96e6c4929b355466ab/mainapp.png)
## ✨ Features

- Full BIN & VLT hash support
  - BIN Memory
  - BIN File
  - VLT Memory
  - VLT File
- Runtime hash table generation
- Accurate OGVI / Attribulator-compatible hashing behavior
- HEX ⇄ DEC synchronized input
- Accepts:
  - Decimal values
  - Hex values (with or without `0x`)
- Copy-to-clipboard on all output fields
- Tooltip preview for truncated strings
- Standalone EXE friendly (no external dependencies at runtime)

---

## 🔄 Old Hash Raider Workflow (Background)

The original NFS Raider workflow (as seen in the classic NFSRaider project)
relied on:

- Predefined hash tables
- Single-field hash resolution
- Limited domain visibility (BIN or VLT at a time)
- Manual context switching when inspecting hashes

While extremely effective for its time, the original approach did not expose
Memory vs File domains simultaneously and required additional tooling for
cross-domain inspection.

NFS Raider v2.0 modernizes this workflow by:
- Generating all hash tables at runtime
- Resolving a single input against all domains at once
- Presenting results side-by-side for immediate comparison
- Maintaining strict compatibility with OGVI / Attribulator logic

Original source:
https://github.com/Felipe379/NFSRaider

---

## 🙏 Credits

- **NFSRaider** — [Felipe379](https://github.com/Felipe379)
- **Attribulator / OGVI** — [NFSTools](https://github.com/NFSTools) & [ARCHIE](https://github.com/ArchieGoldmill)
- **UI Ideas & Inspiration** — Rng_guy  

---

## 📜 License

This project is intended for educational, modding, and preservation purposes
within the Need for Speed community.

---

## 🚀 Notes

If a hash does not resolve, it is because the original string is not present
in the provided symbol list — exactly as Attribulator/OGVI behaves.

Enjoy modding 🚗💨
