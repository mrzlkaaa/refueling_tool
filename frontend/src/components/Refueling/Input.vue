<template>
    <input type="text" :class="[cls ? cls : 'form-control']" v-model="text">
</template>

<script>
export default {
    name: "Input",
    props: {
        cls: String,
    },
    computed:{
        text: {
            get(){
                return ""
            },
            set(val){
                this.$emit("typed", val)
            }
        }
    }
}
</script>