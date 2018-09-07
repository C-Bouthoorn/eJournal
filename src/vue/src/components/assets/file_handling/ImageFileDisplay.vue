<template>
    <div>
        {{ fileName }}
        <icon v-if="!show" @click.native="handleDownload" name="eye" class="action-icon"/>
        <icon v-if="show" @click.native="handleDownload" name="ban" class="crossed-icon"/>
        <icon v-if="show && fileURL" @click.native="downloadLink.click()" name="save" class="action-icon"/>
        <img v-if="show && fileURL" :src="fileURL">
    </div>
</template>

<script>
import userAPI from '@/api/user.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: {
        fileName: {
            required: true,
            String
        },
        authorUID: {
            required: true,
            String
        },
        display: {
            default: false
        }
    },
    components: {
        icon
    },
    data () {
        return {
            show: false,
            fileURL: null,
            downloadLink: null
        }
    },
    methods: {
        handleDownload () {
            this.show = !this.show

            if (!this.fileURL && this.show) {
                this.fileDownload()
            }
        },
        fileDownload () {
            userAPI.download(this.authorUID, this.fileName)
                .then(response => {
                    let blob = new Blob([response.data], { type: response.headers['content-type'] })
                    this.fileURL = window.URL.createObjectURL(blob)

                    this.downloadLink = document.createElement('a')
                    this.downloadLink.href = this.fileURL
                    this.downloadLink.download = this.fileName
                    document.body.appendChild(this.downloadLink)
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
                .catch(_ => {
                    this.$toasted.error('Error creating file.')
                })
        }
    },
    created () {
        this.show = this.display

        if (this.show) { this.fileDownload() }
    },
    destroy () { this.downloadLink.remove() }
}
</script>