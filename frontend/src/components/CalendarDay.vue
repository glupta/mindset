<template>
  <div class="day1">
    <div class="dateindicator">
    <div class="oval"></div>
    <p class="day">28</p>
  </div>
</template>

<script>

export default {
  name: "CalendarDay",
};
</script>

<style scoped>
.day1 {
  background-color: rgba(220, 213, 187, 0.3);
  padding: 20px 20px 45px 126px;
  display: flex;
  align-items: flex-start;
}
.dateindicator {
  padding: 0px 1px 1px 0px;
  display: flex;
  align-items: flex-start;
  position: relative;
}
.oval {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  position: relative;
}
.day {
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  opacity: 0.3;
  position: absolute;
  left: 8px;
  top: 6px;
  letter-spacing: 1px;
}
</style>