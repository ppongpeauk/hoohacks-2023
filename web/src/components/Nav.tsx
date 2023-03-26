import Link from "next/link";
import styles from "./Nav.module.css";

export default function Nav() {
  return (
    <nav className={styles.nav}>
      <div>
        <Link href="/">
          <h2>ResuMatch</h2>
        </Link>
      </div>
    </nav>
  );
}