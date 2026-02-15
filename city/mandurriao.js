intersections = [
    {
        id: "mandurriao - 1",
        name: "Mandurriao - Jaro Rd - Old Iloilo - Capiz Rd",
        latitude: 10.719516,
        longitude: 122.552187,
        connections: ["mandurriao - 2"], //["mandurriao - 2", Infante],
    },
    {
        id: "mandurriao - 2",
        name: "Mandurriao - Jaro Rd - Mandurriao - Sn Miguel Rd",
        latitude: 10.717715,
        longitude: 122.537628,
        connections: ["mandurriao - 1", "mandurriao - 3", "mandurriao - 4"], 
    },
    {
        id: "mandurriao - 3",
        name: "Mandurriao - Sn Miguel Rd - R Mapa St",
        latitude: 10.719233,
        longitude: 122.535611,
        connections: ["mandurriao - 2", "mandurriao - 4"],
    },
    {
        id: "mandurriao - 4",
        name: "R Mapa St - Mandurriao - Jaro Rd",
        latitude: 10.716513,
        longitude: 122.536877,
        connections: ["mandurriao - 2", "mandurriao - 3"],
    },
]

roads = [
    {
        name: "Mandurria - Sn Miguel Rd",
        A: "mandurriao - 3",
        B: "", //Dead - End
        distance: 200,
        lanes: 2,
        one_way: false,
    },
    {
        name: "R Mapa St",
        A: "mandurriao - 4",
        B: "", // To New Carpenter Bridge, Molo
        distance: 1100,
        lanes: 2,
        one_way: false,
    },
    {
        name: "Old Iloilo - Capiz Rd",
        A: "mandurriao - 1", 
        B: "",  // To Infante St, Molo
        distance: 1100,
        lanes: 2,
        one_way: false,
    },
    {
        name: "Mandurriao - Jaro Rd",
        A: "mandurriao - 1",
        B: "mandurriao - 2",
        distance: 1100,
        lanes: 2,
        one_way: false,
    },
    {
        name: "Mandurriao - Jaro Rd - Mandurriao - Sn Miguel Rd",
        A: "mandurriao - 2",
        B: "mandurriao - 3",
        distance: 290,
        lanes: 1,
        one_way: true,
    },
    {
        name: "Mandurriao - Sn Miguel Rd - R Mapa St",
        A: "mandurriao - 3",
        B: "mandurriao - 4",
        distance: 350,
        lanes: 1,
        one_way: true,
    },
    {
        name: "R Mapa St - Mandurriao - Jaro Rd",
        A: "mandurriao - 4",
        B: "mandurriao - 2",
        distance: 170,
        lanes: 1,
        one_way: true,
    },
]