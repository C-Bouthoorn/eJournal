<template>
    <b-form-file
        :accept="acceptedFiletype"
        class="fileinput"
        @change="fileHandler"
        :state="Boolean(file)"
        :placeholder="placeholderText"/>
</template>

<script>
import userAPI from '@/api/user.js'
import escape from '@/utils/escape.js'

export default {
    props: {
        acceptedFiletype: {
            required: true,
            String
        },
        maxSizeBytes: {
            required: true,
            Number
        },
        aID: {
            required: true,
            String
        },
        autoUpload: {
            required: true,
            Boolean
        },
        placeholder: {
            default: 'Select a file.'
        },
        contentID: {
            default: null
        }
    },
    data () {
        return {
            placeholderText: 'Select a file.',
            file: null
        }
    },
    methods: {
        fileHandler (e) {
            let files = e.target.files

            if (!files.length) { return }
            if (files[0].size > this.maxSizeBytes) {
                this.$toasted.error('The selected file exceeds the maximum file size of: ' + this.maxSizeBytes + ' bytes.')
                return
            }

            this.file = files[0]

            this.$emit('fileSelect', this.file.name)

            if (this.autoUpload) { this.uploadFile() }
        },
        uploadFile () {
            let formData = new FormData()
            formData.append('file', this.file)
            formData.append('assignment_id', this.aID)
            formData.append('content_id', this.contentID)

            userAPI.uploadUserFile(formData)
                .then(_ => {
                    this.$emit('fileUploadSuccess', this.file.name)
                    this.$toasted.success('File upload success.')
                })
                .catch(error => {
                    this.$emit('fileUploadFailed', this.file.name)
                    this.$toasted.error(escape(error.response.data.description))
                    this.file = null
                })
        }
    },
    created () {
        // Assume the given file is present in the backend
        if (this.placeholder !== null && this.placeholder !== 'Select a file.') {
            this.file = true
            this.placeholderText = this.placeholder
        }
    }
}
</script>
