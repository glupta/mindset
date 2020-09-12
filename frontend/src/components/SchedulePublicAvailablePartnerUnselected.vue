<template>
  <div class="schedule-public-availablepartner-unselected">
    <div class="background"></div>
    <div class="schedule-public-availablepartner-slot-2">
      <p class="profile-name">Tyson R</p>
      <p class="time">9:00 AM</p>
      <p class="duration">15 min.</p>
    </div>
    <div class="unselected-circle"></div>
  </div>
</template>

<script>
//import { Unselected } from "components";
import Unselected from '@/components/Unselected'

export default {
  name: "SchedulePublicAvailablePartnerUnselected",
  components: { Unselected }
};
</script>

<style scoped>
.schedule-public-availablepartner-unselected {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.background {
  width: 378px;
  height: 32px;
  background-color: rgba(1);
  margin-left: -45px;
  position: relative;
}
.schedule-public-availablepartner-slot-2 {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  position: absolute;
  right: 0px;
  bottom: 2px;
}
.profile-name {
  width: 99px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-transform: uppercase;
  margin-right: 7px;
  letter-spacing: 1px;
}
.time {
  width: 100px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 400;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  margin-right: 13px;
  letter-spacing: 1px;
}
.duration {
  width: 71px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 400;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.unselected-circle {
  position: absolute;
  left: 3px;
  top: 8px;
  width: 14px;
  height: 14px;
  background-color: rgba(250, 251, 251, 1);
  border-radius: 12px;
  border: 1px solid rgba(63, 80, 42, 0.25);
}
</style>