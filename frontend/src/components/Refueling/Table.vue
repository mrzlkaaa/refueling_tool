<template>
    <table class='table table-borderless'>
        <thead>
            <tr>
            <th>6</th>
            <th >5</th>
            <th>4</th>
            <th>3</th>
            </tr>
        </thead>
        <tr v-for="(v,i) in map" v-bind:key="i">
            <td v-for="(vv, ii) in v" v-bind:key="ii">
                {{vv}}
            </td>
            <th> {{7-i}} </th>
        </tr>
    </table>
</template>
<script>
export default {
    name: "Table",
    props: {
        map: Array,
    }
}
</script>