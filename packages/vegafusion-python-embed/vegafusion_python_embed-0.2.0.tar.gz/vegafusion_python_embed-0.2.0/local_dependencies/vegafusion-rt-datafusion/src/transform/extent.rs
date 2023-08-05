/*
 * VegaFusion
 * Copyright (C) 2022 Jon Mease
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License along with this program.
 * If not, see http://www.gnu.org/licenses/.
 */
use crate::expression::compiler::config::CompilationConfig;
use crate::expression::compiler::utils::to_numeric;
use crate::transform::utils::{DataFrameUtils, RecordBatchUtils};
use crate::transform::TransformTrait;
use async_trait::async_trait;
use datafusion::dataframe::DataFrame;
use datafusion::logical_plan::{col, max, min};
use datafusion::scalar::ScalarValue;
use std::sync::Arc;
use vegafusion_core::error::Result;
use vegafusion_core::proto::gen::transforms::Extent;
use vegafusion_core::task_graph::task_value::TaskValue;

#[async_trait]
impl TransformTrait for Extent {
    async fn eval(
        &self,
        dataframe: Arc<DataFrame>,
        _config: &CompilationConfig,
    ) -> Result<(Arc<DataFrame>, Vec<TaskValue>)> {
        let output_values = if self.signal.is_some() {
            let field_col = col(self.field.as_str());
            let min_val =
                min(to_numeric(field_col.clone(), dataframe.schema())?).alias("__min_val");
            let max_val = max(to_numeric(field_col, dataframe.schema())?).alias("__max_val");

            let extent_df = dataframe
                .aggregate(Vec::new(), vec![min_val, max_val])
                .unwrap();

            // Eval to single row dataframe and extract scalar values
            let result_rb = extent_df.collect_flat().await?;
            let min_val_array = result_rb.column_by_name("__min_val")?;
            let max_val_array = result_rb.column_by_name("__max_val")?;

            let min_val_scalar = ScalarValue::try_from_array(min_val_array, 0).unwrap();
            let max_val_scalar = ScalarValue::try_from_array(max_val_array, 0).unwrap();

            // Build two-element list of the extents
            let element_datatype = min_val_scalar.get_datatype();
            let extent_list = TaskValue::Scalar(ScalarValue::List(
                Some(Box::new(vec![min_val_scalar, max_val_scalar])),
                Box::new(element_datatype),
            ));
            vec![extent_list]
        } else {
            Vec::new()
        };

        Ok((dataframe, output_values))
    }
}
