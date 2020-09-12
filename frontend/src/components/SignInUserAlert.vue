<template>
  <div class="signedin">
    <div class="signedin-alertdot"><div class="oval"></div></div>
    <p class="alerttimer">21:47</p>
    <div class="divider"></div>
    <p class="username">Leonetta L.</p>
    <IconsChevronDown></IconsChevronDown>
  </div>
</template>

<script>
import IconsChevronDown from '@/components/IconsChevronDown';

export default {
  name: "SignInUserAlert",
  components: { IconsChevronDown }
};
</script>

<style scoped>
.signedin {
  border-radius: 21px;
  padding: 9px 16px 9px 17px;
  display: flex;
  flex-direction: row;
  align-items: center;
  background: linear-gradient(
    99deg,
    rgba(80, 88, 75, 1) 61%,
    rgba(104, 119, 94, 1) 61%,
    rgba(41, 44, 37, 1) 125%
  );
}
.signedin-alertdot {
  background-color: rgba(255, 91, 91, 1);
  margin-right: 8px;
  border-radius: 50%;
  padding: 6px 5px 5px 6px;
  display: flex;
  align-items: flex-start;
}
.oval {
  width: 5px;
  height: 5px;
  background-color: rgba(238, 242, 244, 1);
  border-radius: 50%;
}
.alerttimer {
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 600;
  line-height: 24px;
  color: rgba(239, 235, 220, 1);
  text-align: center;
  text-transform: uppercase;
  margin-right: 8px;
  letter-spacing: 2px;
}
.divider {
  width: 2px;
  height: 24px;
  background-color: rgba(239, 235, 220, 1);
  margin-right: 7px;
  border-radius: 1px;
}
.username {
  font-family: "Source Sans Pro";
  font-size: 14px;
  font-weight: 600;
  line-height: 24px;
  color: rgba(239, 235, 220, 1);
  text-align: center;
  text-transform: uppercase;
  margin-right: 3px;
  letter-spacing: 2px;
}
</style>