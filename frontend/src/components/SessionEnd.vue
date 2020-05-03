<template>
    <div class='session-end-screen'>
        <p class='header'>
            Your Session Has Ended!
        </p>
        <p class='description'>
            Did your buddy participate in the meditation practice?
        </p>
        <div class='rating-section'>
            <div class='yes-button'>
                <div class='thumbs-up'></div>
                <p class='yes-text'>
                    Yes
                </p>
            </div>
            <div class='no-button'>
                <div class='thumbs-down'></div>
                <p class='no-text'>
                    No
                </p>
            </div>
        </div>
        <div class='schedule-appointment-button'>
            <p class="schedule-appointment-text">
                Make Another Appointment
            </p>
        </div>
    </div>
</template>

<script>
export default {
  name: 'SessionEnd',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
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
</style>