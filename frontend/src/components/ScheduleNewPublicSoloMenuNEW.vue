<template>
  <div class="schedule-newpublicsolomenu-new">
    <p class="sessionoptions-text">
      Select from available times  or schedule your own!
    </p>
    <div :class="{'session-active': public_bool, 'session-inactive': new_bool}" @click='onSelectPublic'>
      <p class="public-sessions">PUBLIC SESSIONS</p>
      <img class="icons-chevron-right" src="@/assets/img/chevron-right.svg"/>
    </div>
    <div :class="{'session-active': new_bool, 'session-inactive': public_bool}" @click='onSelectNew'>
      <p class="new-session">NEW SESSION</p>
      <img class="icons-chevron-right" src="@/assets/img/chevron-right.svg"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScheduleNewPublicSoloMenuNEW',
  data () {
    return {
      public_bool: true,
      new_bool: false
    }
  },
  methods: {
    onSelectPublic() {
      this.new_bool = false;
      this.public_bool = true;
      this.$emit('select-public');
    },
    onSelectNew() {
      this.new_bool = true;
      this.public_bool = false;
      this.$emit('select-new');
    }
  }
};
</script>

<style scoped>
.sessionoptions-text {
  width: 260px;
  font-family: "Source Sans Pro";
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(51, 46, 45, 1);
  text-align: center;
  letter-spacing: 2px;
  margin-bottom: 24px;
}
.schedule-newpublicsolomenu-new {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.public-sessions {
  width: 176px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  margin-right: 9px;
  letter-spacing: 1px;
}
.session-inactive {
  background-color: rgba(250, 251, 251, 1);
  opacity: 0.5;
  padding: 11px 12px 12px 19px;
  display: flex;
  flex-direction: row;
  align-items: center;
  cursor: pointer;
}
.session-active {
  padding: 11px 12px 12px 19px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  background: linear-gradient(
    96deg,
    rgba(239, 235, 220, 1) 41%,
    rgba(191, 180, 139, 1) 160%
  );
}
.new-session {
  width: 176px;
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  margin-right: 9px;
  letter-spacing: 1px;
}
.icons-chevron-right {
  margin-top: 2px;
  width: 24px;
  height: 24px;
}
.schedule-newpublicsolomenu-public {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
</style>