<template>
    <div class="schedule-session">
        <NavBar></NavBar>
        <p class='header'>
            Pick a time that works for you
        </p>
        <div class='email-input'></div>
        <div class='select-day'></div>
        <div class='select-time'></div>
        <div class='submit-button'>
            <p class="submit-button-text">
                Submit
            </p>
        </div>
    </div>
</template>

<script>
export default {
  name: 'ScheduleSession',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
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
</style>
