import Link from "next/link";
import styles from "./Nav.module.css";

export default function Nav() {
  return (
    <nav className={styles.nav}>
      <div>
        <Link href="/">
          <h1>LinkedOut</h1>
        </Link>
      </div>
    </nav>
  );
}