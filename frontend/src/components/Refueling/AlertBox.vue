<template>
    <div :class="[code < 400 ? 'alert alert-success' : 'alert alert-danger']" role="alert">
        {{ code!=400 ? text+'. You will be redirect in few seconds' : 'ERROR: ' + text}}
    </div>
</template>
<script>
export default {
    name: "AlertBox", 
    props:["code", "text"],
}
</script>