import React from "react";
import styles from "./Expand.module.css";

const Expand = ({
  vector = "https://static.overlay-tech.com/assets/da3240da-bd38-4970-9700-774d24526a4c.svg"
}) => {
  return (
    <div className={styles.frame}>
      <img alt="" className={styles.vector} src={vector} />
    </div>
  );
};

export default Expand;