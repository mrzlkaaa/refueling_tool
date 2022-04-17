<template>
    <div class="form-check form-switch">
        <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" :checked="status" 
            @change="$emit('toggleCheckbox')">
        <label class="form-check-label" for="flexSwitchCheckDefault">{{text}}</label>
    </div>
</template>
<script>
export default {
    name: "Checkbox",
    props: ["status", "text"],
}
</script>
<style>
</style>