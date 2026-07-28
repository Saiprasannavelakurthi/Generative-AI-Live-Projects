import { AnimatePresence, motion } from 'framer-motion';

/**
 * TransitionShell
 * ----------------
 * Wraps DynamicCodeRenderer's output states (idle/downloading/compiling/live/error)
 * and animates the handoff between the "staticUI" (placeholder/skeleton shown
 * before or while code is being fetched/compiled) and the "generatedUI"
 * (the freshly compiled Component) so the swap never pops or jumps.
 *
 * Design goals:
 *  - No hard unmount/remount flash: AnimatePresence + mode="wait" ensures the
 *    outgoing view fully exits before the incoming view enters.
 *  - No layout jump: the wrapping motion.div uses the `layout` prop so height/
 *    width changes between static and generated content animate smoothly
 *    instead of snapping.
 *  - Distinct but related motion per state: static -> generated crossfades
 *    with a slight scale + blur "focus in" (implies "something resolved"),
 *    while error states use a soft shake-free fade so failures don't feel
 *    alarming.
 */

const EASE = [0.4, 0, 0.2, 1]; // standard Material-style ease, avoids overshoot

const variants = {
  initial: { opacity: 0, y: 8, scale: 0.98, filter: 'blur(4px)' },
  animate: { opacity: 1, y: 0, scale: 1, filter: 'blur(0px)' },
  exit: { opacity: 0, y: -6, scale: 0.99, filter: 'blur(2px)' },
};

const skeletonVariants = {
  initial: { opacity: 0 },
  animate: {
    opacity: [0.5, 0.9, 0.5],
    transition: { duration: 1.4, repeat: Infinity, ease: 'easeInOut' },
  },
  exit: { opacity: 0, transition: { duration: 0.15 } },
};

const TRANSITION = { duration: 0.38, ease: EASE };

/**
 * @param {'idle'|'downloading'|'compiling'|'live'|'error'} status
 * @param {React.ReactNode} staticUI       - shown for idle/downloading/compiling
 * @param {React.ComponentType|null} generatedComponent - compiled Component, shown when status === 'live'
 * @param {React.ReactNode} errorPanel     - shown when status === 'error'
 * @param {object} scope                   - extra props forwarded to the generated component
 */
export default function TransitionShell({
  status,
  staticUI,
  generatedComponent: GeneratedComponent,
  errorPanel,
  scope = {},
}) {
  const isLive = status === 'live' && GeneratedComponent;
  const isError = status === 'error';
  const isLoading = status === 'downloading' || status === 'compiling';

  // A single stable key per "view" is what lets AnimatePresence detect the
  // swap and animate it, rather than re-rendering the same node in place.
  const viewKey = isLive ? 'generated' : isError ? 'error' : 'static';

  return (
    <div className="relative w-full">
      <AnimatePresence mode="wait" initial={false}>
        <motion.div
          key={viewKey}
          layout
          variants={variants}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={TRANSITION}
          className="w-full"
        >
          {viewKey === 'generated' && <GeneratedComponent {...scope} />}

          {viewKey === 'error' && errorPanel}

          {viewKey === 'static' && (
            <motion.div
              variants={isLoading ? skeletonVariants : undefined}
              initial="initial"
              animate="animate"
              exit="exit"
            >
              {staticUI}
            </motion.div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
