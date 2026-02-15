intersections = [
  {
    id: "Molo - 1",
    name: "Locsin St - New Carpenter's Bridge",
    latitude: 10.699186,
    longitude: 122.542524,
    connections: ["Molo - 2"], // + connect outside sa molo
  },
  {
    id: "Molo - 2",
    name: "Locsin St - San Jose St.",
    latitude: 10.698215,
    longitude: 122.542886,
    connections: ["Molo - 1", "Molo - 3"],
  },
  {
    id: "Molo - 3",
    name: "Locsin St - San Marcos St.",
    latitude: 10.697347,
    longitude: 122.543396,
    connections: ["Molo - 2, Molo - 4"],
  },

  {
    id: "Molo - 4",
    name: "Locsin St. - M.H Del Pilar St. 2",
    latitude: 10.695993,
    longitude: 122.544452,
    connections: ["Molo - 3", "Molo - 5"],
  },
  {
    id: "Molo - 5",
    name: "Locsin St. - Timawa St.",
    latitude: 10.694449,
    longitude: 122.545638,
    connections: ["Molo - 4", "Molo - 6"],
  },
  {
    id: "Molo - 6",
    name: "Locsin St. - Baluarte - Calumpag - Villa - Oton Blvd",
    latitude: 10.692042,
    longitude: 122.549359,
    connections: ["Molo - 5"],
  },
  {
    id: "Molo - 7",
    name: "San Marcos St. - MH del Pilar St. 1",
    latitude: 10.699243,
    longitude: 122.549363,
    connections: ["Molo - 3"],
  }, 
];

roads = [];
