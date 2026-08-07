import { AnimatePresence, motion } from "framer-motion";

/**
 * TransitionShell
 *
 * Smoothly transitions between:
 * - idle
 * - downloading
 * - compiling
 * - live
 * - error
 */

const EASE = [0.4, 0, 0.2, 1];

const PAGE_TRANSITION = {
  duration: 0.35,
  ease: EASE,
};

const pageVariants = {
  initial: {
    opacity: 0,
    y: 8,
    scale: 0.98,
    filter: "blur(4px)",
  },

  animate: {
    opacity: 1,
    y: 0,
    scale: 1,
    filter: "blur(0px)",
  },

  exit: {
    opacity: 0,
    y: -8,
    scale: 0.99,
    filter: "blur(2px)",
  },
};

const loadingVariants = {
  initial: {
    opacity: 0.5,
  },

  animate: {
    opacity: [0.45, 1, 0.45],

    transition: {
      duration: 1.4,
      repeat: Infinity,
      ease: "easeInOut",
    },
  },

  exit: {
    opacity: 0,
    transition: {
      duration: 0.15,
    },
  },
};

export default function TransitionShell({
  status,
  staticUI,
  generatedComponent: GeneratedComponent,
  errorPanel,
  scope = {},
}) {
  const isLoading =
    status === "downloading" ||
    status === "compiling";

  const isLive =
    status === "live" &&
    Boolean(GeneratedComponent);

  const isError =
    status === "error";

  let view = "static";

  if (isLive) {
    view = "generated";
  } else if (isError) {
    view = "error";
  }

  const renderContent = () => {
    switch (view) {
      case "generated":
        return (
          <GeneratedComponent
            {...scope}
          />
        );

      case "error":
        return errorPanel;

      default:
        return (
          <motion.div
            variants={
              isLoading
                ? loadingVariants
                : undefined
            }
            initial="initial"
            animate="animate"
            exit="exit"
          >
            {staticUI}
          </motion.div>
        );
    }
  };

  return (
    <div className="relative w-full overflow-hidden">
      <AnimatePresence
        mode="wait"
        initial={false}
      >
        <motion.div
          key={view}
          layout
          variants={pageVariants}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={PAGE_TRANSITION}
          className="w-full"
        >
          {renderContent()}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}