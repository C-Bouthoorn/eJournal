/**
 * Replace all characters which might be used to inject HTML with their corresponding special character.
 * If the rawhtml is not a string, it won't get changed.
 */
export function escapeHtml (rawhtml) {
    if (typeof rawhtml !== 'string') {
        return rawhtml
    }

    // Based on https://stackoverflow.com/a/4835406
    const specialCharacterMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }

    return rawhtml.replace(/[&<>"']/g, (match) => specialCharacterMap[match])
}
