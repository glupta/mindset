<template>
  <div class="navbar flexCR space-between">
    <img class="logo" src="@/assets/mhlogo.png">
    <!-- <div class='hamburger-menu flexCC'>
      <div class='rounded-shape'></div>
      <div class='rounded-shape'></div>
      <div class='rounded-shape'></div>
    </div> -->
  </div>
</template>

<script>
export default {
  name: 'Navbar',
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

.navbar {
  padding-left: 11px;
  padding-right: 23px;
  height: 60px;
  background-color: #FFFFFF;
  box-shadow: 0px 4px 5px rgba(0,0,0,0.25);
  align-items: center;
}

.logo {
  width: 38px;
  height: 40px;
}

.hamburger-menu {
  width: 19px;
  height: 15px;
}

.rounded-shape {
  position: absolute;
  left: 12.5%;
  right: 12.5%;
  top: 75%;
  bottom: 25%;
  border: 2.66667px solid rgba(0, 0, 0, 0.05);
  width: 19px;
  height: 2px;
  background-color: rgba(0, 0, 0, 0.05);
  padding-top: 3px;
  padding-bottom: 3px;
}
</style>
