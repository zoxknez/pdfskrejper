# UI Fixes - Summary

## Changes Made

### 1️⃣ **Files Page - Added Search Button**
**File:** `templates/files.html`

**Problem:** Search input field bez dugmeta za pokretanje pretrage

**Solution:**
- Changed search input width from `col-md-8` to `col-md-6`
- Added new `col-md-2` column with Search button
- Button has ID `filterBtn` for JavaScript functionality

**Code:**
```html
<!-- Search Button -->
<div class="col-md-2 d-flex align-items-end">
    <button type="button" class="btn btn-primary w-100" id="filterBtn">
        <i class="bi bi-search"></i> <span data-i18n="files.filter.submit">Filtriraj</span>
    </button>
</div>
```

---

### 2️⃣ **Navbar - Added Logout Icon**
**File:** `templates/base.html`

**Problem:** Logout samo u dropdown meniju

**Solution:**
- Added direct logout icon in navbar (next to language toggle)
- Keeps dropdown menu intact (for profile + logout text)
- Icon: `bi-box-arrow-right`

**Code:**
```html
<!-- Logout Icon (Direct) -->
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('logout') }}" title="Odjavi se">
        <i class="bi bi-box-arrow-right"></i>
    </a>
</li>
```

---

### 3️⃣ **Footer - Removed Extra Icons**
**File:** `templates/base.html`

**Problem:** Footer imao "testuser" + theme/language/logout ikonice (višak)

**Solution:**
- **Removed:** Theme toggle icon from footer
- **Removed:** Language toggle icon from footer
- **Removed:** Username display from footer
- **Removed:** Logout icon from footer
- **Kept:** Copyright + Social links (GitHub, Email, PayPal)

**Before:**
```
[Copyright]  [GitHub][Email][PayPal]  [Theme][Lang][testuser][Logout]
```

**After:**
```
[Copyright]  [GitHub][Email][PayPal]
```

---

### 4️⃣ **Language Toggle - Renamed GB → EN**
**File:** `static/js/language.js`

**Problem:** Language toggle pokazivao "🇬🇧" emoji (GB flag)

**Solution:**
- Changed from emoji flags to text abbreviations
- SRB (Serbian) ↔ EN (English)

**Code Change:**
```javascript
// BEFORE:
langFlag.textContent = this.currentLang === 'sr' ? '🇷🇸' : '🇬🇧';

// AFTER:
langFlag.textContent = this.currentLang === 'sr' ? 'SRB' : 'EN';
```

---

## Files Modified

| File | Changes |
|------|---------|
| `templates/files.html` | Added Search button (1 change) |
| `templates/base.html` | Added navbar logout icon + cleaned footer (2 changes) |
| `static/js/language.js` | Changed emoji flags to text (1 change) |

**Total:** 4 changes across 3 files

---

## Testing Checklist

- [ ] **Files page** - Search button appears and works
- [ ] **Navbar** - Logout icon visible (next to language toggle)
- [ ] **Footer** - Only copyright + social links (no theme/lang/user/logout)
- [ ] **Language toggle** - Shows "SRB" and switches to "EN" (not 🇬🇧)
- [ ] **Logout** - Both navbar icon and dropdown work

---

## Expected Result

### Navbar (Right side):
```
[☀️ Theme]  [SRB/EN]  [👤 testuser ▼]  [🚪 Logout Icon]
```

### Footer:
```
© 2025 PDF Skrejper. Sva prava zadržana.    [GitHub] [Email] [PayPal]
```

### Files Page - Filter Row:
```
[Category Dropdown] [Search Input] [🔍 Filtriraj Button]
```

---

## Notes

- Logout now accessible from **3 places**:
  1. Navbar logout icon (new)
  2. User dropdown → "Odjavi se" (existing)
  3. ~~Footer logout icon~~ (removed)

- Language toggle now shows **text** (SRB/EN) instead of emoji flags
- Footer decluttered - only copyright + social links remain
- Search button has `data-i18n="files.filter.submit"` for i18n support
