<template>
    <div class='session-end-screen'>
      <NavBar></NavBar>
        <p class='header'>
            Your Session Has Ended!
        </p>
        <p class='description'>
            Did your buddy participate in the meditation practice?
        </p>
        <div class='rating-section'>
            <div class='yes-button' v-bind:class="{ active: yesSelected}"  v-on:click='onSelectYes()'>
                <div class='thumbs-up'></div>
                <p class='yes-text'>
                    Yes
                </p>
            </div>
            <div class='no-button' v-bind:class="{ active: noSelected }"  v-on:click='onSelectNo()'>
                <div class='thumbs-down'></div>
                <p class='no-text'>
                    No
                </p>
            </div>
        </div>
        <div class='schedule-appointment-button' v-on:click='goToScheduleSession()'>
            <p class="schedule-appointment-text">
                Make Another Appointment
            </p>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar'
import router from '../router'
export default {
  name: 'SessionEnd',
  data () {
    return {
      yesSelected: false,
      noSelected: false
    }
  },
  components: {
    NavBar
  },
  methods: {
    onSelectYes() {
      this.noSelected = false;
      this.yesSelected = true;
    },
    onSelectNo() {
      this.yesSelected = false;
      this.noSelected = true;
    },
    goToScheduleSession() {
      router.push({ name: "ScheduleSession" })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.active {
  background-color: #18A0FB;
}
</style>