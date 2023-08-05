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
use crate::expression::compiler::builtin_functions::date_time::date_parsing::{
    datetime_strs_to_millis, DateParseMode,
};

use crate::expression::compiler::call::LocalTransformFn;
use chrono::{DateTime, Datelike, NaiveDateTime, TimeZone, Timelike, Weekday};
use datafusion::arrow::array::{Array, ArrayRef, Date32Array, Int64Array, StringArray};
use datafusion::arrow::compute::cast;
use datafusion::arrow::datatypes::{DataType, TimeUnit};
use datafusion::logical_plan::{DFSchema, Expr};
use datafusion::physical_plan::functions::{make_scalar_function, Signature, Volatility};
use datafusion::physical_plan::udf::ScalarUDF;
use datafusion_expr::ReturnTypeFunction;
use std::sync::Arc;
use vegafusion_core::arrow::compute::unary;
use vegafusion_core::error::Result;

#[inline(always)]
pub fn extract_year(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    dt.year() as i64
}

#[inline(always)]
pub fn extract_month(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    dt.month0() as i64
}

#[inline(always)]
pub fn extract_quarter(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    (dt.month0() as f64 / 3.0).floor() as i64 + 1
}

#[inline(always)]
pub fn extract_date(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    dt.day() as i64
}

#[inline(always)]
pub fn extract_day(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    let weekday = dt.weekday();
    if matches!(weekday, Weekday::Sun) {
        0
    } else {
        weekday as i64 + 1
    }
}

#[inline(always)]
pub fn extract_dayofyear(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    dt.ordinal() as i64
}

#[inline(always)]
pub fn extract_hour(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    dt.hour() as i64
}

#[inline(always)]
pub fn extract_minute(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    dt.minute() as i64
}

#[inline(always)]
pub fn extract_second(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    dt.second() as i64
}

#[inline(always)]
pub fn extract_millisecond(dt: &DateTime<chrono_tz::Tz>) -> i64 {
    dt.nanosecond() as i64 / 1000000
}

fn process_input_datetime(arg: &ArrayRef, tz: &chrono_tz::Tz) -> ArrayRef {
    match arg.data_type() {
        DataType::Utf8 => {
            let array = arg.as_any().downcast_ref::<StringArray>().unwrap();
            datetime_strs_to_millis(array, DateParseMode::JavaScript, &Some(*tz)) as _
        }
        DataType::Date32 => {
            let ms_per_day = 1000 * 60 * 60 * 24_i64;
            let array = arg.as_any().downcast_ref::<Date32Array>().unwrap();

            let array: Int64Array = unary(array, |v| (v as i64) * ms_per_day);
            Arc::new(array) as ArrayRef as _
        }
        DataType::Date64 => {
            let int_array = cast(arg, &DataType::Int64).unwrap();
            int_array
        }
        DataType::Int64 => arg.clone(),
        _ => panic!("Unexpected data type for date part function:"),
    }
}

pub fn make_local_datepart_transform(
    extract_fn: fn(&DateTime<chrono_tz::Tz>) -> i64,
    name: &str,
) -> LocalTransformFn {
    let name = name.to_string();
    let local_datepart_transform =
        move |local_tz: chrono_tz::Tz, args: &[Expr], _schema: &DFSchema| -> Result<Expr> {
            let udf = make_datepart_udf(local_tz, extract_fn, &name);
            Ok(Expr::ScalarUDF {
                fun: Arc::new(udf),
                args: Vec::from(args),
            })
        };
    Arc::new(local_datepart_transform)
}

pub fn make_datepart_udf(
    tz: chrono_tz::Tz,
    extract_fn: fn(&DateTime<chrono_tz::Tz>) -> i64,
    name: &str,
) -> ScalarUDF {
    let part_fn = move |args: &[ArrayRef]| {
        // Signature ensures there is a single argument
        let arg = &args[0];
        let arg = process_input_datetime(arg, &tz);

        let mut result_builder = Int64Array::builder(arg.len());

        let arg = arg.as_any().downcast_ref::<Int64Array>().unwrap();
        for i in 0..arg.len() {
            if arg.is_null(i) {
                result_builder.append_null().unwrap();
            } else {
                let utc_millis = arg.value(i);
                let utc_seconds = utc_millis / 1_000;
                let utc_nanos = (utc_millis % 1_000 * 1_000_000) as u32;
                let naive_utc_datetime = NaiveDateTime::from_timestamp(utc_seconds, utc_nanos);
                let datetime = tz.from_utc_datetime(&naive_utc_datetime);
                let value = extract_fn(&datetime);
                result_builder.append_value(value).unwrap();
            }
        }

        Ok(Arc::new(result_builder.finish()) as ArrayRef)
    };
    let part_fn = make_scalar_function(part_fn);

    let return_type: ReturnTypeFunction = Arc::new(move |_| Ok(Arc::new(DataType::Int64)));
    ScalarUDF::new(
        name,
        &Signature::uniform(
            1,
            vec![
                DataType::Utf8,
                DataType::Timestamp(TimeUnit::Millisecond, None),
                DataType::Date32,
                DataType::Date64,
                DataType::Int64,
            ],
            Volatility::Immutable,
        ),
        &return_type,
        &part_fn,
    )
}

lazy_static! {
    // Local
    pub static ref YEAR_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_year, "year");
    pub static ref MONTH_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_month, "month");
    pub static ref QUARTER_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_quarter, "quarter");
    pub static ref DATE_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_date, "date");
    pub static ref DAYOFYEAR_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_dayofyear, "dayofyear");
    pub static ref DAY_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_day, "day");
    pub static ref HOURS_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_hour, "hours");
    pub static ref MINUTES_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_minute, "minutes");
    pub static ref SECONDS_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_second, "seconds");
    pub static ref MILLISECONDS_TRANSFORM: LocalTransformFn =
        make_local_datepart_transform(extract_millisecond, "milliseconds");

    // UTC
    pub static ref UTCYEAR_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_year, "utcyear");
    pub static ref UTCMONTH_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_month, "utcmonth");
    pub static ref UTCQUARTER_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_quarter, "utcquarter");
    pub static ref UTCDATE_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_date, "utcdate");
    pub static ref UTCDAYOFYEAR_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_dayofyear, "utcdayofyear");
    pub static ref UTCDAY_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_day, "utcday");
    pub static ref UTCHOURS_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_hour, "utchours");
    pub static ref UTCMINUTES_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_minute, "utcminutes");
    pub static ref UTCSECONDS_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_second, "utcseconds");
    pub static ref UTCMILLISECONDS_UDF: ScalarUDF =
        make_datepart_udf(chrono_tz::UTC, extract_millisecond, "utcmilliseconds");
}
