<template>
    <div id="app">
        <header-bar/>
        <router-view :key="$route.path" class="min-height-100"/>
        <feedback-section/>
    </div>
</template>

<script>
import Header from '@/Header'
import FeedbackSection from '@/FeedbackSection'

export default {
    components: {
        'header-bar': Header,
        'feedback-section': FeedbackSection
    }
}
</script>

<style lang="sass">
@import '~sass/global.sass'
@import '~sass/modules/breakpoints.sass'

#app
    overflow-x: hidden
    font-family: 'Roboto', sans-serif
    font-size: 1em
    -webkit-font-smoothing: antialiased
    -moz-osx-font-smoothing: grayscale
    padding-top: 70px
    min-height: 100%

    @include lg
        height: 100%
</style>
