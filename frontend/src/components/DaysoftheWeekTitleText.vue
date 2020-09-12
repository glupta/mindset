<template>
  <div class="daysoftheweek-title">
    <div class="weekdays"><p class="weekdaytext">Sun</p></div>
    <div class="weekdays"><p class="text">Mon</p></div>
    <div class="weekdays"><p class="text">Tue</p></div>
    <div class="weekdays"><p class="text">Wed</p></div>
    <div class="weekdays"><p class="text">Thu</p></div>
    <div class="weekdays"><p class="text">Fri</p></div>
    <div class="weekdays"><p class="text">Sat</p></div>
  </div>
</template>

<script>

export default {
  name: "DaysoftheWeekTitleText",
};
</script>

<style scoped>
.daysoftheweek-title {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin-bottom: 7px;
}
.weekdays {
  background-color: rgba(250, 251, 251, 1);
  padding: 8px 0px 5px;
  width: 186px;
  display: flex;
  align-items: flex-start;
  margin: 0 1px;
}
.weekdaytext {
  width: 186px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>