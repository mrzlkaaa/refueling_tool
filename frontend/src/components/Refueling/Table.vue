<template>
    <table class='table'>
        <thead>
            <tr>
            <th scope="col">6</th>
            <th scope="col">5</th>
            <th scope="col">4</th>
            <th scope="col">3</th>
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