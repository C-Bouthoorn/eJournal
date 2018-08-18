import Vue from 'vue'
import App from './App'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import '../node_modules/bootstrap/dist/css/bootstrap.css'
import '../node_modules/bootstrap-vue/dist/bootstrap-vue.css'

import 'vue-awesome/icons/eye'
import 'vue-awesome/icons/caret-up'
import 'vue-awesome/icons/caret-down'
import 'vue-awesome/icons/arrows'
import 'vue-awesome/icons/trash'
import 'vue-awesome/icons/plus-square'
import 'vue-awesome/icons/hourglass-half'
import 'vue-awesome/icons/check'
import 'vue-awesome/icons/times'
import 'vue-awesome/icons/exclamation'
import 'vue-awesome/icons/plus'
import 'vue-awesome/icons/list-ul'
import 'vue-awesome/icons/paper-plane'
import 'vue-awesome/icons/save'
import 'vue-awesome/icons/upload'
import 'vue-awesome/icons/download'
import 'vue-awesome/icons/arrow-right'
import 'vue-awesome/icons/arrow-left'
import 'vue-awesome/icons/user'
import 'vue-awesome/icons/users'
import 'vue-awesome/icons/shield'
import 'vue-awesome/icons/user-times'
import 'vue-awesome/icons/user-plus'
import 'vue-awesome/icons/edit'
import 'vue-awesome/icons/undo'
import 'vue-awesome/icons/sign-in'
import 'vue-awesome/icons/sign-out'
import 'vue-awesome/icons/ban'
import 'vue-awesome/icons/link'
import 'vue-awesome/icons/envelope'
import 'vue-awesome/icons/home'
import 'vue-awesome/icons/calendar'
import 'vue-awesome/icons/question'

import Toasted from 'vue-toasted'

Vue.config.productionTip = false
Vue.use(Toasted, { position: 'bottom-right', duration: 4000 })
Vue.use(BootstrapVue)

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    data: {
        colors: ['pink-border', 'peach-border', 'blue-border'],
        generalPermissions: {},
        assignmentPermissions: {},
        validToken: false,
        previousPage: null,
        windowWidth: 0,
        maxFileSizeBytes: 2097152
    },
    mounted () {
        this.$nextTick(function () {
            window.addEventListener('resize', this.getWindowWidth)

            this.getWindowWidth()
        })
    },
    beforeDestroy () {
        window.removeEventListener('resize', this.getWindowWidth)
    },
    methods: {
        getWindowWidth () {
            this.windowWidth = window.innerWidth
        },
        /* Bootstrap breakpoints for custom events. */
        // TODO Figure out how to get these from the dedicated sass file (more webpack fun)
        sm () { return this.windowWidth > 575 },
        md () { return this.windowWidth > 767 },
        lg () { return this.windowWidth > 991 },
        xl () { return this.windowWidth > 1199 },
        xsMax () { return this.windowWidth < 576 },
        smMax () { return this.windowWidth < 769 },
        mdMax () { return this.windowWidth < 992 },
        lgMax () { return this.windowWidth < 1200 },
        timeLeft (date) {
            /* Date format is:
             * Returns the remaining time left as:
             * If the time left is negative returns Expired
             * TODO implement (will most likely require a lib) */
            return '1M 9D 9H'
        },
        getBorderClass (cID) {
            return this.colors[cID % this.colors.length]
        },
        beautifyDate (date) {
            if (!date) {
                return ''
            }

            var year = date.substring(0, 4)
            var month = date.substring(5, 7)
            var day = date.substring(8, 10)
            var time = date.substring(11, 16)

            return day + '-' + month + '-' + year + ' ' + time
        },

        /* #############################################################
         *              Permissions,
         * Front-end interface for all possible permissions.
         * For an overview see:
         * https://docs.google.com/spreadsheets/d/1M7KnEKL3cG9PMWfQi9HIpRJ5xUMou4Y2plnRgke--Tk
         *
         * ##############################################################
         */

        /* Site-wide permissions */
        isAdmin () {
            return this.generalPermissions.is_superuser
        },
        /* Institute wide settings, think institute name/abbreviation logo. */
        canEditInstitute () {
            return this.generalPermissions.can_edit_institute
        },

        /* Course level based permissions. These permissions are enabled and
        used per course. */

        /* Course permissions. */
        canEditCourseRoles () {
            return this.generalPermissions.can_edit_course_roles
        },
        canAddCourse () {
            return this.generalPermissions.can_add_course
        },
        canViewCourseParticipants () {
            return this.generalPermissions.can_view_course_participants
        },
        canAddCourseParticipants () {
            return this.generalPermissions.can_add_course_participants
        },
        canEditCourse () {
            return this.generalPermissions.can_edit_course
        },
        canDeleteCourse () {
            return this.generalPermissions.can_delete_course
        },
        canAddAssignment () {
            return this.generalPermissions.can_add_assignment
        },

        /* Assignment permissions. */
        canEditAssignment () {
            return this.assignmentPermissions.can_edit_assignment
        },
        canViewAssignmentParticipants () {
            return this.assignmentPermissions.can_view_assignment_participants
        },
        canDeleteAssignment () {
            return this.assignmentPermissions.can_delete_assignment
        },
        canPublishAssignmentGrades () {
            return this.assignmentPermissions.can_publish_assignment_grades
        },

        /* Grade permissions. */
        canGradeJournal () {
            return this.assignmentPermissions.can_grade_journal
        },
        canPublishJournalGrades () {
            return this.assignmentPermissions.can_publish_journal_grades
        },
        canEditJournal () {
            return this.assignmentPermissions.can_edit_journal
        },
        canCommentJournal () {
            return this.assignmentPermissions.can_comment_journal
        }
    },
    template: '<App/>'
})
