export default {
    /**
     * Replace all characters which might be used to inject HTML with their corresponding special character.
     */
    escapeHtml: (rawhtml) {
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
}
