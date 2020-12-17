import GateDashboard from "./views/GateDashboard";
import CCTVDashboard from "./views/CCTVDashboard";
import COVIDDashboard from "./views/COVIDDashboard";

var dashRoutes = [
  {
    path: "/covid19",
    name: "COVID19",
    icon: "media-2_sound-wave", 
    component: COVIDDashboard,
    layout: "/admin",
  },
  {
    path: "/gatedashboard",
    name: "Gate",
    icon: "ui-1_lock-circle-open",
    component: GateDashboard,
    layout: "/admin",
  },
  {
    path: "/cctvdashboard",
    name: "CCTV",
    icon: "media-1_camera-compact",
    component: CCTVDashboard,
    layout: "/admin",
  },
];
export default dashRoutes;
