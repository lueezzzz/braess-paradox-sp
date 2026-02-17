intersections = [
  {
    id: "lapuz - 1",
    name: "Divinagracia St - Railroad St",
    latitude: 10.707280,
    longitude: 122.5715728,
    connections: ["lapaz - 4", "lapuz -3 "], 
  },
  {
    id: "lapuz - 2",
    name: "Rizal St - Quirino-Lopez Bridge",
    latitude: 10.7022611,
    longitude: 122.5714736,
    connections: ["lapaz - 2", "lapuz - 4"], //["lapaz - 2", "lapuz - 4", quirino-lopez bridge]
  },
  {
    id: "lapuz - 3",
    name: "Railroad St - Abanilla St",
    latitude: 10.7031872,
    longitude: 122.5739868,
    connections: ["lapuz - 1", "lapuz - 4"],
  },
  {
    id: "lapuz - 4",
    name: "Abanilla St - Rizal St",
    latitude: 10.7017996,
    longitude: 122.5753356,
    connections: ["lapuz - 2", "lapuz - 3", "lapuz - 5"],
  },
  {
    id: "lapuz - 5",
    name: "Rizal St - New Iloilo Ferry Terminal Access Rd",
    latitude: 10.7017752,
    longitude: 122.5768179,
    connections: ["lapuz - 4", "lapuz - 6"],
  },
  {
    id: "lapuz - 6",
    name: "Rizal St - Lapuz-Mansaya-Roboc Rd",
    latitude: 10.6985812,
    longitude: 122.5820938,
    connections: ["lapuz - 5", "lapuz - 7"],
  },
  {
    id: "lapuz - 7",
    name: "Rizal St - Iloilo Airport Direct Rd",
    latitude: 10.7060003,
    longitude: 122.5887091,
    connections: ["lapuz - 6", "lapaz - 9"],
  },
];

roads = [
  {
    name: "Railroad St",
    A: "lapuz - 1",
    B: "lapuz - 3",
    distance: 550,
    lanes: 2,
    one_way: false,
  },
  {
    name: "Abanilla St",
    A: "lapuz - 3",
    B: "lapuz - 4",
    distance: 240,
    lanes: 2,
    one_way: false,
  },
  {
    name: "Rizal St - Lapuz-Mansaya-Loboc Rd",
    A: "lapaz - 2", 
    B: "lapuz - 6",
    distance: 1300,
    lanes: 2,
    one_way: false,
  },
  {
    name: "Rizal St - New Iloilo Ferry Terminal Access Rd",
    A: "lapuz - 5",
    B: "", //Dead End
    distance: 600,
    lanes: 2,
    one_way: false,
  },
  {
    name: "Rizal St - Iloilo Airport Direct Rd",
    A: "lapuz - 5",
    B: "", //Dead End
    distance: 240,
    lanes: 2,
    one_way: false,
  },
];
